from wsgi.app_handlers import static_file
from wsgi.calendars import caldav_api
from wsgi.calendars.conference import Conference
from wsgi.database import db
from wsgi.bots.mm_bot import MMBot
from wsgi.schedulers.sd import scheduler, delete_jobs_by_user_id
from wsgi.settings import MM_BOT_OPTIONS
from wsgi.converters import get_dt_with_UTC_tz_from_iso

import logging, caldav, traceback
from caldav import Calendar
from datetime import datetime, timedelta, UTC


def change_status_job(user_id: str, expires_at: str):
    bot = MMBot(MM_BOT_OPTIONS)
    bot.login()

    try:

        bot_update_user_status_custom = bot.update_user_status_custom(
            user_id=user_id,
            options={
                'emoji': 'calendar',
                'text': 'In a meeting',
                'expires_at': expires_at,  # ISO 8601 format
            })

    except IOError as exp:
        logging.error(
            'Error bot_update_user_status_custom with user_id=%s. Traceback: ```%s```',
            user_id, traceback.format_exc(),
        )

    else:

        bot.logout()


def notify_next_conference_job(user_id: str, calendar_name: str, uid: str, before_10_min: bool,
                               change_status: bool) -> None:
    user = db.User.get_user(user_id)

    if not user:
        delete_jobs_by_user_id(user_id)
        logging.info(f'Delete jobs with {user_id=}. User doesn\'t exist')
        return

    bot = MMBot(MM_BOT_OPTIONS)
    bot_login = bot.login()

    bot_channel = bot.channels.create_direct_message_channel([user_id, bot_login['id']])

    represents = caldav_api.first_conference_notification(user, calendar_name)

    if represents.get('type') != 'ok':

        delete_jobs_by_user_id(user_id)
        message = 'Your notify scheduler was deleted. Please, create notify again'

    else:

        message = 'Hi, I remind you that you have a conference in 10 minutes!'

    first_conferences = represents.get('first_conferences')
    cal = represents.get('cal')

    before_status_job_id = f'{user_id}(before-status)'

    if not first_conferences:

        delete_jobs_by_user_id(user_id)

        pretext = 'Empty list upcoming conferences'

        bot_create_post = bot.posts.create_post({

            'channel_id': bot_channel['id'],
            'message': message,
            "props": {
                "attachments": [
                    {
                        "fallback": "test",
                        "title": "Yandex Calendar(upcoming conference)",
                        "pretext": pretext,
                        "text": represents.get('text'),
                        "thumb_url": static_file('ya.png')
                    }
                ]},

        })

        return

    elif is_exist_conference_at_time(cal, first_conferences, uid, user.timezone):

        if before_10_min is True:
            pretext = 'Upcoming conference!'

            bot_create_post = bot.posts.create_post({

                'channel_id': bot_channel['id'],
                'message': message,
                "props": {
                    "attachments": [
                        {
                            "fallback": "test",
                            "title": "Yandex Calendar(upcoming conference)",
                            "pretext": pretext,
                            "text": represents.get('text'),
                            "thumb_url": static_file('ya.png')
                        }
                    ]},

            })

        if change_status is True:
            next_conf = first_conferences[0]

            job_change_status_id = f'{user_id}(change-status)'

            scheduler.add_job(
                func=change_status_job,
                trigger='date',
                args=(user_id, next_conf.dtend),
                id=job_change_status_id,
                name=user.login,
                replace_existing=True,
                run_date=next_conf.dtstart,


            )

    for next_conference in first_conferences[1:]:

        if conference_start_gt_15_min(next_conference):
            start_job = get_dt_with_UTC_tz_from_iso(next_conference.dtstart)

            scheduler.add_job(

                func=notify_next_conference_job,
                trigger='date',
                args=(user_id, calendar_name, next_conference.uid, before_10_min, change_status),
                name=user.login,
                id=before_status_job_id,
                replace_existing=True,
                run_date=start_job - timedelta(minutes=10),

            )

            break

    bot.logout()


def daily_notification_job(user_id: str, calendar_name: str):
    bot = MMBot(MM_BOT_OPTIONS)
    bot_login = bot.login()

    user = db.User.get_user(user_id)

    if not user:
        delete_jobs_by_user_id(user_id)
        logging.info(f'Delete jobs with {user_id=}.User doesn\'t exist')
        return

    body_conferences = caldav_api.daily_notification(user, calendar_name)

    if body_conferences.get('type') != 'ok':

        delete_jobs_by_user_id(user_id)
        message = 'Your jobs was deleted. Please, create notify again'

    else:

        message = '# Hi, I sent you a list of the conferences for today'

    bot_channel = bot.channels.create_direct_message_channel([bot_login['id'], user_id])

    bot_create_post = bot.posts.create_post({
        'channel_id': bot_channel['id'],
        'message': message,
        "props": {
            "attachments": [
                {
                    "fallback": "test",
                    "title": "Yandex Calendar(daily)",
                    "pretext": "Daily notify!",
                    "text": body_conferences.get('text'),
                    "thumb_url": static_file('ya.png')
                }
            ]},
    })

    bot.logout()


def is_exist_conference_at_time(cal: Calendar, first_conferences: list[Conference, ...], uid: str,
                                timezone: str) -> bool:
    conf_obj = first_conferences[0]

    try:

        event = cal.event_by_uid(uid)

    except caldav.lib.error.NotFoundError as exp:

        return False

    else:

        conference = Conference(event.icalendar_component, timezone)

        start_point = datetime.now(UTC)
        middle_point = get_dt_with_UTC_tz_from_iso(conference.dtstart)
        end_point = start_point + timedelta(minutes=15)

        return conference.uid == conf_obj.uid and start_point < middle_point < end_point


def conference_start_gt_15_min(conference: Conference):
    start_point = get_dt_with_UTC_tz_from_iso(conference.dtstart)
    end_point = datetime.now(UTC) + timedelta(minutes=15)

    return start_point > end_point
