import asyncio, json, logging
from datetime import timedelta, datetime
from dramatiq import actor
import caldav.lib.error as caldav_errors
from caldav import SynchronizableCalendarObjectCollection as SyncCal, Principal
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncConnection

from ..app_handlers import static_file
from ..bots.bot_commands import send_msg_client, update_custom_status, get_user_by_mm_user_id
from ..calendars import caldav_api, caldav_filters
from ..calendars.caldav_funcs import take_principal
from ..calendars.conference import Conference
from ..converters import (
    get_dt_with_UTC_tz_from_iso, iso1_gt_iso2, dont_clear, create_conference_table, create_row_table, equal_conferences,
    get_delay_with_dtstart, get_delay_daily
)
from ..notifications import notification_views
from ..sql_app.crud import YandexConference, YandexCalendar, User
from ..sql_app.database import get_conn
from ..notifications.worker import *

# dramatiq app.notifications.tasks

logging.basicConfig(level=Conf.LOG_LEVEL)


async def task0():
    """check_events_job"""
    logging.debug('check_events_job')
    await check_events_job()


# task-daily
@actor(max_retries=1)
async def task1(mm_user_id: str, hour: int, minute: int):
    """daily_notification_job"""
    logging.debug('daily_notification_job(%s, %s, %s)', mm_user_id, hour, minute)
    await daily_notification_job(mm_user_id, hour, minute)


# task-next-conf
@actor(max_retries=1)
async def task2(mm_user_id: str, uid: str, dtstart: str):
    """notify_next_conference_job"""
    logging.debug('notify_next_conference_job(%s, %s, %s)', mm_user_id, uid, dtstart)
    await notify_next_conference_job(mm_user_id, uid, dtstart)


@actor(max_retries=1)
async def task3(mm_user_id: str, expires_at: str):
    """change_status_job"""
    logging.debug('change_status_job(%s, %s)', mm_user_id, expires_at)
    await change_status_job(mm_user_id, expires_at)


@actor(max_retries=1)
async def task4(mm_user_id: str, latest_custom_status: str):
    """return_latest_custom_status_job"""
    logging.debug('return_latest_custom_status_job(%s, %s)', mm_user_id, latest_custom_status)
    await return_latest_custom_status_job(mm_user_id, latest_custom_status)


async def _load_changes_events(conn: AsyncConnection, principal: Principal, user: Row, get_user_cal: Row):
    not_sync_cal = await caldav_api.get_calendar_by_cal_id(principal, cal_id=get_user_cal.cal_id)

    # get sync_token from db

    try:

        sync_cal = await asyncio.to_thread(
            not_sync_cal.objects_by_sync_token, sync_token=get_user_cal.sync_token, load_objects=True
        )

    except caldav_errors.NotFoundError as exp:
        await YandexCalendar.remove_cals(conn, user.mm_user_id)

    else:
        # update sync_token in db
        await YandexCalendar.update_cal(conn, get_user_cal.cal_id, sync_token=sync_cal.sync_token)

        await load_updated_added_deleted_events(conn, user, sync_cal)


async def check_events_job():
    async with get_conn() as conn:
        async for user in User.all_users(conn):
            principal = await take_principal(user.login, user.token)
            if type(principal) is dict:

                await User.remove_user(conn, user.mm_user_id)
                continue

            else:

                async for get_user_cal in YandexCalendar.get_cals(conn, user.mm_user_id):
                    await _load_changes_events(conn, principal, user, get_user_cal)


async def return_latest_custom_status_job(mm_user_id: str, latest_custom_status: str):
    async with get_conn() as conn:
        user = await User.get_user(conn, mm_user_id)

        if not user:
            return

        elif user.status != latest_custom_status:
            return

        else:
            await User.update_user(conn, mm_user_id, status=None)

            options = json.loads(latest_custom_status)

            asyncio.create_task(update_custom_status(mm_user_id, options))


async def change_status_job(mm_user_id: str, expires_at: str):
    """{'props': {'customStatus': '{"emoji":"grinning","text":"","duration":"date_and_time","expires_at":"2023-08-16T10:30:00Z"}'}'"""

    async with get_conn() as conn:
        user = await User.get_user(conn, mm_user_id)

        if not user:
            return

        mm_user = await get_user_by_mm_user_id(mm_user_id)

        run_date = datetime.fromisoformat(expires_at)
        delay = get_delay_with_dtstart(run_date)

        new_options = {"emoji": "calendar", 'text': 'In a meeting', 'expires_at': expires_at}
        props = mm_user.get('props', {})

        if not props:
            props['customStatus'] = ''

        if not props.get('customStatus'):

            current_options = {}

        else:

            current_options = json.loads(props.get('customStatus'))

        if current_options:

            current_options.setdefault('text', current_options['emoji'])

            if dont_clear(current_options['expires_at']):

                current_options = {'emoji': current_options['emoji'], 'text': current_options['text']}

                js_current_options = json.dumps(current_options)

                if user.status != js_current_options:
                    await User.update_user(conn, mm_user_id, status=js_current_options)

                task4.send_with_options(args=(mm_user_id, js_current_options), delay=delay)

                asyncio.create_task(update_custom_status(mm_user_id, new_options))

            elif iso1_gt_iso2(current_options['expires_at'], expires_at) and current_options['emoji'] != 'calendar':

                js_current_options = json.dumps(current_options)

                if user.status != js_current_options:
                    await User.update_user(conn, mm_user_id, status=js_current_options)

                task4.send_with_options(args=(mm_user_id, js_current_options), delay=delay)

                asyncio.create_task(update_custom_status(mm_user_id, new_options))

        if current_options.get('expires_at') is None or iso1_gt_iso2(expires_at, current_options['expires_at']):
            asyncio.create_task(update_custom_status(mm_user_id, new_options))


async def notify_next_conference_job(mm_user_id: str, uid: str, dtstart: str) -> None:
    async with get_conn() as conn:
        user = await User.get_user(conn, mm_user_id)

        if not user:
            return

        principal = await take_principal(user.login, user.token)

        if type(principal) is dict:
            await User.remove_user(conn, mm_user_id)

            return

        user_conf = await YandexConference.get_conference(conn, uid)

        if not user_conf:
            return

        cal = await caldav_api.get_calendar_by_cal_id(principal, cal_id=user_conf.cal_id)

        try:

            event = await asyncio.to_thread(cal.event_by_uid, uid=uid)

        except caldav_errors.NotFoundError as exp:

            await YandexConference.remove_conference(conn, uid=uid)

            return

        i_event = event.icalendar_component

        if i_event.get('X-TELEMOST-CONFERENCE'):

            conf_obj = Conference(i_event, user.timezone)
            # if conference.dtstart has modified than skip send email
            if dtstart != conf_obj.dtstart:
                return

            if caldav_filters.is_exist_conf_at_time(conf_obj.dtstart):
                if user.e_c:
                    pretext = 'Upcoming conference!'
                    msg = '### Bot send notification!'

                    represents = await notification_views.notify_next_conference_view(
                        'first_conference.md', str(cal), conf_obj
                    )
                    props = {
                        "attachments": [
                            {
                                "fallback": "test",
                                "color": '#21FA2E',
                                "title": "Yandex Calendar(upcoming conference)",
                                "pretext": pretext,
                                "text": represents.get('text'),
                                "thumb_url": static_file('ya.png'),
                            }
                        ]}
                    asyncio.create_task(send_msg_client(mm_user_id, msg, props))

                if user.ch_stat:
                    delay = get_delay_with_dtstart(datetime.fromisoformat(conf_obj.dtstart))

                    task3.send_with_options(args=(mm_user_id, conf_obj.dtend,), delay=delay)


async def daily_notification_job(mm_user_id: str, hour: int, minute: int):
    async with get_conn() as conn:
        user = await User.get_user(conn, mm_user_id)

        if not user:
            return

        principal = await take_principal(user.login, user.token)

        if type(principal) is dict:
            await User.remove_user(conn, mm_user_id)
            asyncio.create_task(send_msg_client(mm_user_id, principal.get('text')))
            return

        if not await YandexCalendar.get_first_cal(conn, mm_user_id):
            return

        exists_db_server_cals = await caldav_api.check_exist_calendars_by_cal_id(
            conn, principal, YandexCalendar.get_cals(conn, mm_user_id)
        )

        if type(exists_db_server_cals) is dict:
            return

        body_conferences = await caldav_api.daily_notification(principal, user, exists_db_server_cals)

        msg = '# Hi, I sent you a list of the conferences for today'
        props = {
            "attachments": [
                {
                    "fallback": "test",
                    "color": '#21FA2E',
                    "title": "Yandex Calendar(daily)",
                    "pretext": "Daily notify!",
                    "text": body_conferences.get('text'),
                    "thumb_url": static_file('ya.png')
                }
            ]}

        asyncio.create_task(send_msg_client(mm_user_id, msg, props))

        delay = get_delay_daily(hour, minute)
        task1.send_with_options(args=(mm_user_id, hour, minute), delay=delay)


async def load_updated_added_deleted_events(
        conn: AsyncConnection,
        user: Row,
        sync_cal: SyncCal,
        notify=True
):
    mm_user_id = user.mm_user_id
    cal_id = sync_cal.calendar.id
    calendar_name = str(sync_cal.calendar)

    for sync_event in sync_cal:
        # if deleted conference
        if not sync_event.data:

            canonical_url = sync_event.canonical_url

            uid = canonical_url.split('/')[-1].removesuffix('.ics')

            deleted_conf = await YandexConference.remove_conference(conn, uid)

            if deleted_conf:
                if notify is True:
                    was_table = create_row_table(deleted_conf)

                    represents = await notification_views.notify_loaded_conference_view(
                        'loaded_conference.md', calendar_name, 'deleted', was_table, None
                    )

                    asyncio.create_task(send_msg_client(mm_user_id, represents.get('text')))

            continue

        i_event = sync_event.icalendar_component

        if i_event.get('X-TELEMOST-CONFERENCE'):

            conf = Conference(i_event, user.timezone)
            get_conf_user = await YandexConference.get_conference(conn, conf.uid)

            str_organizer = ', '.join(f'{k} - {v}' for k, v in conf.organizer.items()) if conf.organizer else None
            str_attendee = "; ".join(", ".join(f"{attr} - {value}" for attr, value in a.items()) for a in
                                     conf.attendee) if conf.attendee else None

            # if added conference
            if not get_conf_user:
                await YandexConference.add_conference(
                    conn,
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

                if notify is True:
                    new_table = create_conference_table(conf)
                    represents = await notification_views.notify_loaded_conference_view(
                        "loaded_conference.md", calendar_name, "added", None, new_table
                    )

                    asyncio.create_task(send_msg_client(mm_user_id, represents.get('text')))

            # if changed conference
            elif get_conf_user and not equal_conferences(get_conf_user, conf):

                await YandexConference.update_conference(
                    conn,
                    conf.uid,
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

                if notify is True:
                    was_table = create_row_table(get_conf_user)
                    new_table = create_conference_table(conf)

                    represents = await notification_views.notify_loaded_conference_view(
                        "loaded_conference.md", calendar_name, "updated", was_table, new_table
                    )

                    asyncio.create_task(send_msg_client(mm_user_id, represents.get('text')))

            # else conference is exists
            else:
                continue

            # new conference + user e_c or ch_stat + start date > now + 15 min
            if Conf.TESTING:
                if (user.e_c or user.ch_stat) and caldav_filters.start_gt_now(conf.dtstart):  # debug
                    start_job = get_dt_with_UTC_tz_from_iso(conf.dtstart) - timedelta(seconds=10)  # debug

                    delay = get_delay_with_dtstart(start_job)
                    task2.send_with_options(args=(mm_user_id, conf.uid, conf.dtstart), delay=delay)
            else:
                if (user.e_c or user.ch_stat) and caldav_filters.start_gt_15_min(conf.dtstart):  # production
                    start_job = get_dt_with_UTC_tz_from_iso(conf.dtstart) - timedelta(minutes=10)  # production

                    delay = get_delay_with_dtstart(start_job)
                    task2.send_with_options(args=(mm_user_id, conf.uid, conf.dtstart), delay=delay)
