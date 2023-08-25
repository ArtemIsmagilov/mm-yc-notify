from wsgi.app_handlers import static_file
from wsgi.calendars import caldav_api, caldav_filters
from wsgi.calendars.conference import Conference
from wsgi.database import db
from wsgi.notifications import notification_views
from wsgi.schedulers import sd
from wsgi.converters import get_dt_with_UTC_tz_from_iso, iso1_gt_iso2, dont_clear, create_conference_table, create_row_table
from wsgi.bots.mm_bot import bot, send_msg_client

import logging, json, traceback
from datetime import timedelta
from sqlalchemy.engine import Row
from caldav import SynchronizableCalendarObjectCollection as SyncCal
import caldav.lib.error as caldav_errs
from httpx import HTTPError


def check_events_job(mm_user_id):
    user = db.User.get_user(mm_user_id=mm_user_id)

    if not user:
        sd.delete_jobs_by_mm_user_id(mm_user_id)

        logging.info(f'Delete jobs with {mm_user_id=}. User doesn\'t exist')

        return

    principal = caldav_api.take_principal(user)

    if type(principal) is dict:

        sd.delete_jobs_by_mm_user_id(mm_user_id)
        db.User.remove_user(mm_user_id=mm_user_id)

        logging.info(f'Delete jobs with {mm_user_id=}. Incorrect username and token')

        msg = ('Incorrect username and token. '
               'Write in `connections` correct username and token. Your notifications was deleted. '
               'Please, again create connections in command `connections create`.')

        send_msg_client(mm_user_id, msg)

        return

    cal_ids = [c.cal_id for c in db.YandexCalendar.get_cals(user_id=user.id)]

    for cal_id in cal_ids:

        cal = principal.calendar(cal_id=cal_id)
        # get sync_token from db
        get_user_cal = db.YandexCalendar.get_cal(cal_id=cal_id)

        try:

            sync_cal = cal.objects_by_sync_token(sync_token=get_user_cal.sync_token, load_objects=True)

        except caldav_errs.NotFoundError as exp:

            sd.delete_jobs_by_cal_id(cal_id)
            removed_cal = db.YandexCalendar.remove_cals(user_id=user.id)

            send_msg_client(mm_user_id, f'Delete jobs with {cal_id=}. Calendar with {cal_id=} isn\'t exist.')

            logging.info(f'Delete jobs with {cal_id=}. Calendar with {cal_id=} isn\'t exist.')

        else:
            load_updated_added_deleted_events(user, sync_cal)
            # update sync_token in db
            db.YandexCalendar.update_cal(cal_id, sync_token=sync_cal.sync_token)


def return_latest_custom_status_job(mm_user_id: str, latest_custom_status: str):
    options = json.loads(latest_custom_status)

    try:

        bot_patch_user = bot.status.update_user_custom_status(mm_user_id, options)

    except HTTPError as exp:

        logging.error(
            'Error with mm_user_id=%s. <###traceback###\n%s\n###traceback###>\n\n',
            mm_user_id,
            traceback.format_exc(),
        )


def change_status_job(mm_user_id: str, expires_at: str):
    """{'props': {'customStatus': '{"emoji":"grinning","text":"","duration":"date_and_time","expires_at":"2023-08-16T10:30:00Z"}'}'"""
    try:

        bot_get_user = bot.users.get_user(mm_user_id)

    except HTTPError as exp:

        logging.error('Error with user_id=%s. <###traceback###\n%s###traceback###>',
                      mm_user_id,
                      traceback.format_exc())

        return

    new_options = {"emoji": "calendar", 'text': 'In a meeting', 'expires_at': expires_at}
    props = bot_get_user.get('props', {})

    if not props:
        props['customStatus'] = ''

    if not props.get('customStatus'):

        latest_options = {}

    else:

        latest_options = json.loads(props.get('customStatus'))

    if latest_options:

        latest_options.setdefault('text', latest_options['emoji'])

        if dont_clear(latest_options['expires_at']):

            latest_options = {'emoji': latest_options['emoji'], 'text':latest_options['text']}

            sd.delete_rt_stat_job(mm_user_id)

            sd.scheduler.add_job(
                func=return_latest_custom_status_job,
                trigger='date',
                args=(mm_user_id, json.dumps(latest_options)),
                id=f'{mm_user_id}(rt_stat)',
                replace_existing=True,
                run_date=expires_at,
            )

        elif iso1_gt_iso2(latest_options['expires_at'], expires_at):

            sd.delete_rt_stat_job(mm_user_id)

            sd.scheduler.add_job(
                func=return_latest_custom_status_job,
                trigger='date',
                args=(mm_user_id, json.dumps(latest_options)),
                id=f'{mm_user_id}(rt_stat)',
                replace_existing=True,
                run_date=expires_at,
            )

    try:

        bot_update_user_custom_status = bot.status.update_user_custom_status(mm_user_id, new_options)

    except HTTPError as exp:

        logging.error('Error with user_id=%s. <###traceback###\n%s###traceback###>',
                      mm_user_id,
                      traceback.format_exc())


def notify_next_conference_job(mm_user_id: str, uid: str) -> None:
    user = db.User.get_user(mm_user_id=mm_user_id)

    if not user:

        sd.delete_jobs_by_mm_user_id(mm_user_id)
        logging.info(f'Delete jobs with {mm_user_id=}. User doesn\'t exist')

        return

    principal = caldav_api.take_principal(user)

    if type(principal) is dict:

        sd.delete_jobs_by_mm_user_id(mm_user_id)
        db.User.remove_user(mm_user_id=mm_user_id)

        logging.info(f'Delete jobs with {mm_user_id=}. Incorrect username and token')

        msg = ('Incorrect username and token. '
               'Write in `connections` correct username and token. Your notifications was deleted. '
               'Please, again create notifications in command `notifications create`.')

        send_msg_client(mm_user_id, msg)

        return

    # TODO create custom sql query
    user_conf = db.YandexConference.get_conference(uid=uid)
    get_user_cal = db.YandexCalendar.get_cal(cal_id=user_conf.cal_id)
    
    cal = principal.calendar(cal_id=get_user_cal.cal_id)

    try:

        event = cal.event_by_uid(uid=uid)

    except caldav_errs.NotFoundError as exp:
        logging.info(f'Calendar with {get_user_cal.cal_id=} not found event with {uid=}')
        db.YandexConference.remove_conference(uid=uid)
        sd.delete_job_by_uid(uid)

        return

    else:
        i_event = event.icalendar_component

        if i_event.get('X-TELEMOST-CONFERENCE'):

            conf_obj = Conference(i_event, user.timezone)

            if caldav_filters.is_exist_conf_at_time(conf_obj.dtstart):
                if user.e_c:
                    pretext = 'Upcoming conference!'
                    msg = '### Bot send notification!'

                    represents = notification_views.notify_next_conference_view(
                        'first_conference.md', cal.get_display_name(), conf_obj
                    )

                    try:

                        bot_create_direct_channel = bot.channels.create_direct_channel(
                            [mm_user_id, bot.client.userid])

                        bot_create_post = bot.posts.create_post({
                            'channel_id': bot_create_direct_channel['id'],
                            'message': msg,
                            "props": {
                                "attachments": [
                                    {
                                        "fallback": "test",
                                        "title": "Yandex Calendar(upcoming conference)",
                                        "pretext": pretext,
                                        "text": represents.get('text'),
                                        "thumb_url": static_file('ya.png'),
                                    }
                                ]},
                        })

                    except HTTPError as exp:

                        logging.error(
                            'Error with mm_user_id=%s. <###traceback###\n%s\n###traceback###>\n\n',
                            mm_user_id,
                            traceback.format_exc(),
                        )

                if user.ch_stat:
                    job = sd.scheduler.add_job(
                        func=change_status_job,
                        trigger='date',
                        args=(mm_user_id, conf_obj.dtend),
                        id=f'{mm_user_id}-{get_user_cal.cal_id}-{uid}(ch_stat)',
                        name=user.login,
                        replace_existing=True,
                        run_date=conf_obj.dtstart,
                    )

            else:
                logging.info(
                    f'Conference with {uid=} is exist for user with {mm_user_id=}, but conference out of notice.')


def daily_notification_job(mm_user_id: str):
    user = db.User.get_user(mm_user_id=mm_user_id)

    if not user:
        sd.delete_jobs_by_mm_user_id(mm_user_id)
        logging.info(f'Delete jobs with {mm_user_id=}.User doesn\'t exist')

        return

    cals_id = [row.cal_id for row in db.YandexCalendar.get_cals(user_id=user.id)]

    exists_cals = caldav_api.check_exist_calendars_by_cal_id(user, cals_id)

    if type(exists_cals) is dict:

        body_conferences = exists_cals

    else:

        body_conferences = caldav_api.daily_notification(user, exists_cals)

    if body_conferences.get('type') != 'ok':

        sd.delete_jobs_by_cal_id(mm_user_id)
        db.YandexCalendar.remove_cals(user_id=user.id)

        msg = f'Delete jobs with {mm_user_id=}. Your server does not have the before selected calendars. Need again create notifications'

    else:

        msg = '# Hi, I sent you a list of the conferences for today'

    try:

        bot_create_direct_channel = bot.channels.create_direct_channel([mm_user_id, bot.client.userid])

        bot_create_post = bot.posts.create_post({
            'channel_id': bot_create_direct_channel['id'],
            'message': msg,
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

    except HTTPError as exp:

        logging.error(
            'Error with mm_user_id=%s. <###traceback###\n%s\n###traceback###>\n\n',
            mm_user_id,
            traceback.format_exc(),
        )


def load_updated_added_deleted_events(user: Row, sync_cal: SyncCal, notify=True):

    mm_user_id = user.mm_user_id
    cal_id = sync_cal.calendar.id
    print(sync_cal.objects)
    for sync_event in sync_cal:
        # if deleted conference
        if not sync_event.data:

            canonical_url = sync_event.canonical_url

            uid = canonical_url.split('/')[-1].removesuffix('.ics')

            sd.delete_job_by_uid(uid)
            deleted_conf = db.YandexConference.remove_conference(uid=uid)

            if deleted_conf:

                was_table = create_row_table(deleted_conf)

                represents = notification_views.notify_loaded_conference_view(
                    'loaded_conference.md', sync_cal.calendar.get_display_name(), 'deleted', was_table, None
                )

                if notify is True:
                    send_msg_client(mm_user_id, represents.get('text'))

            continue

        i_event = sync_event.icalendar_component

        if i_event.get('X-TELEMOST-CONFERENCE'):

            conf = Conference(i_event, user.timezone)

            str_organizer = 'name - {}, email - {}'.format(conf.organizer.get('name'), conf.organizer.get('email')) if conf.organizer else None
            str_attendee = "; ".join(", ".join(f"{attr} - {value}" for attr, value in a.items()) for a in conf.attendee) if conf.attendee else None

            get_conf_user = db.YandexConference.get_conference(uid=conf.uid)

            # if changed conference
            if get_conf_user:

                db.YandexConference.update_conference(conf.uid,
                    cal_id=cal_id,
                    timezone=conf.timezone,
                    dtstart=conf.dtstart,
                    dtend=conf.dtend,
                    summary=conf.summary,
                    created=conf.created,
                    last_modified=conf.last_modified,
                    description=conf.description,
                    url_event=conf.url_event,
                    categories=conf.categories,
                    x_telemost_conference=conf.x_telemost_conference,
                    organizer=str_organizer,
                    attendee=str_attendee,
                    location=conf.location,
                )

                was_table = create_row_table(get_conf_user)
                new_table = create_conference_table(conf)

                represents = notification_views.notify_loaded_conference_view(
                    "loaded_conference.md", sync_cal.calendar.get_display_name(), "updated", was_table, new_table
                )

                if notify is True:
                    send_msg_client(mm_user_id, represents.get('text'))

            # else added conference
            else:

                db.YandexConference.add_conference(
                    cal_id=cal_id,
                    uid=conf.uid,
                    timezone=conf.timezone,
                    dtstart=conf.dtstart,
                    dtend=conf.dtend,
                    summary=conf.summary,
                    created=conf.created,
                    last_modified=conf.last_modified,
                    description=conf.description,
                    url_event=conf.url_event,
                    categories=conf.categories,
                    x_telemost_conference=conf.x_telemost_conference,
                    organizer=str_organizer,
                    attendee=str_attendee,
                    location=conf.location,
                )

                new_table = create_conference_table(conf)

                represents = notification_views.notify_loaded_conference_view(
                    "loaded_conference.md", sync_cal.calendar.get_display_name(), "added", None, new_table
                )

                if notify is True:
                    send_msg_client(mm_user_id, represents.get('text'))

            if (user.e_c or user.ch_stat) and caldav_filters.start_gt_15_min(conf.dtstart):
                start_job = get_dt_with_UTC_tz_from_iso(conf.dtstart) - timedelta(minutes=10)

                job1 = sd.scheduler.add_job(
                    func=notify_next_conference_job,
                    trigger='date',
                    args=(mm_user_id, conf.uid),
                    id=f'{mm_user_id}-{cal_id}-{conf.uid}(next_conf)',
                    name=user.login,
                    replace_existing=True,
                    run_date=start_job,
                )
