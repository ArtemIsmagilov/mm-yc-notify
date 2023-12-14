import asyncio, json, logging
from dramatiq import actor
from textwrap import shorten
from datetime import timedelta, datetime
import caldav.lib.error as caldav_errors
from caldav import Principal, Calendar
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Sequence
from ..app_handlers import static_file
from ..async_wraps.async_wrap_caldav import (
    caldav_calendar_by_cal_id, caldav_event_by_uid
)
from ..bots.bot_commands import send_msg_client, update_custom_status, get_user_by_mm_user_id
from ..calendars import caldav_api, caldav_filters
from ..calendars.caldav_funcs import take_principal
from ..calendars.caldav_searchers import find_conferences_in_one_cal
from ..calendars.conference import Conference
from ..converters import (
    get_dt_with_UTC_tz_from_iso, iso1_gt_iso2, dont_clear, create_conference_table, create_row_table, equal_conferences,
    get_delay_with_dtstart, get_delay_daily, conference_all_day, past_conference
)
from ..notifications import notification_views
from ..schemas import UserView
from ..sql_app.crud import YandexConference, YandexCalendar, User
from ..sql_app.database import get_conn
from ..notifications.worker import *
from zoneinfo import ZoneInfo
from settings import Conf


async def task0():
    """check_events_job"""
    logging.debug('check_events_job')
    await check_events_job()


@actor(max_retries=1)
async def task1(session: str, hour: int, minute: int):
    """daily_notification_job"""
    logging.debug('daily_notification_job(%s, %s, %s)', session, hour, minute)
    await daily_notification_job(session, hour, minute)


@actor(max_retries=1)
async def task2(session: str, uid: str, dtstart: str):
    """notify_next_conference_job"""
    logging.debug('notify_next_conference_job(%s, %s, %s)', session, uid, dtstart)
    await notify_next_conference_job(session, uid, dtstart)


@actor(max_retries=1)
async def task3(session: str, expires_at: str):
    """change_status_job"""
    logging.debug('change_status_job(%s, %s)', session, expires_at)
    await change_status_job(session, expires_at)


@actor(max_retries=1)
async def task4(session: str, latest_custom_status: str):
    """return_latest_custom_status_job"""
    logging.debug('return_latest_custom_status_job(%s, %s)', session, latest_custom_status)
    await return_latest_custom_status_job(session, latest_custom_status)


async def _load_changes_events(conn: AsyncConnection, principal: Principal, user: UserView, user_cal_in_db: Row):
    cal_in_server = await caldav_calendar_by_cal_id(principal, cal_id=user_cal_in_db.cal_id)

    dt_start = datetime(1970, 1, 1, tzinfo=ZoneInfo(user.timezone))
    dt_end = datetime(2050, 1, 1, tzinfo=ZoneInfo(user.timezone))

    try:
        cal_confs = await find_conferences_in_one_cal(cal_in_server, (dt_start, dt_end))

    except caldav_errors.NotFoundError as exp:
        await YandexCalendar.remove_cal(conn, user_cal_in_db.cal_id)

    else:
        if cal_confs:
            await load_updated_added_deleted_events(conn, user, cal_confs)


async def check_events_job():
    async with get_conn() as conn:
        async for user in User.all_users(conn):
            user_view = UserView(
                user.mm_user_id,
                user.login,
                user.token,
                user.timezone,
                user.e_c,
                user.ch_stat,
                user.session,
                user.status
            )
            principal = await take_principal(user_view.login, user_view.token)
            if type(principal) is dict:

                await User.remove_user(conn, user_view.mm_user_id)
                continue

            else:

                async for cal_in_db in YandexCalendar.get_cals(conn, user_view.mm_user_id):
                    await _load_changes_events(conn, principal, user_view, cal_in_db)


async def return_latest_custom_status_job(session: str, latest_custom_status: str):
    async with get_conn() as conn:
        user = await User.get_user_by_session(conn, session)

        if not user:
            return

        elif user.status != latest_custom_status:
            return

        else:
            await User.update_user(conn, user.mm_user_id, status=None)

            options = json.loads(latest_custom_status)

            asyncio.create_task(update_custom_status(user.mm_user_id, options))


async def change_status_job(session: str, expires_at: str):
    """{'props': {'customStatus': '{"emoji":"grinning","text":"","duration":"date_and_time","expires_at":"2023-08-16T10:30:00Z"}'}'"""

    async with get_conn() as conn:
        user = await User.get_user_by_session(conn, session)

        if not user:
            return

        mm_user = await get_user_by_mm_user_id(user.mm_user_id)

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
                    await User.update_user(conn, user.mm_user_id, status=js_current_options)

                await task4.send_with_options(args=(session, js_current_options), delay=delay)

                asyncio.create_task(update_custom_status(user.mm_user_id, new_options))

            elif iso1_gt_iso2(current_options['expires_at'], expires_at) and current_options['emoji'] != 'calendar':

                js_current_options = json.dumps(current_options)

                if user.status != js_current_options:
                    await User.update_user(conn, user.mm_user_id, status=js_current_options)

                await task4.send_with_options(args=(session, js_current_options), delay=delay)

                asyncio.create_task(update_custom_status(user.mm_user_id, new_options))

        if current_options.get('expires_at') is None or iso1_gt_iso2(expires_at, current_options['expires_at']):
            asyncio.create_task(update_custom_status(user.mm_user_id, new_options))


async def notify_next_conference_job(session: str, uid: str, dtstart: str) -> None:
    async with get_conn() as conn:
        user = await User.get_user_by_session(conn, session)

        if not user:
            return

        principal = await take_principal(user.login, user.token)

        if type(principal) is dict:
            await User.remove_user(conn, user.mm_user_id)

            return

        conf_in_db = await YandexConference.get_conference(conn, uid)

        if not conf_in_db:
            return

        cal = await caldav_calendar_by_cal_id(principal, cal_id=conf_in_db.cal_id)

        try:

            event = await caldav_event_by_uid(cal, uid=uid)

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
                    asyncio.create_task(send_msg_client(user.mm_user_id, msg, props))

                if user.ch_stat:
                    delay = get_delay_with_dtstart(datetime.fromisoformat(conf_obj.dtstart))

                    task3.send_with_options(args=(session, conf_obj.dtend), delay=delay)


async def daily_notification_job(session: str, hour: int, minute: int):
    async with get_conn() as conn:
        user = await User.get_user_by_session(conn, session)

        if not user:
            return

        principal = await take_principal(user.login, user.token)

        if type(principal) is dict:
            await User.remove_user(conn, user.mm_user_id)
            return

        if not await YandexCalendar.get_first_cal(conn, user.mm_user_id):
            return

        exists_db_server_cals = await caldav_api.check_exist_calendars_by_cal_id(
            conn, principal, YandexCalendar.get_cals(conn, user.mm_user_id)
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

        asyncio.create_task(send_msg_client(user.mm_user_id, msg, props))

        delay = get_delay_daily(hour, minute)
        task1.send_with_options(args=(session, hour, minute), delay=delay)


async def load_updated_added_deleted_events(
        conn: AsyncConnection,
        user: UserView,
        cal_confs: tuple[Calendar, Sequence[Conference]] | None,
        notify=True
):
    if not cal_confs:
        return
    cal, confs = cal_confs
    mm_user_id = user.mm_user_id
    cal_id = cal.id
    calendar_name = str(cal)
    conf_uids = set()
    for c in confs:
        conf_uids.add(c.uid)
        str_organizer = ', '.join(f'{k} - {v}' for k, v in c.organizer.items()) if c.organizer else 'None'
        str_attendee = "; ".join(", ".join(f"{attr} - {value}" for attr, value in a.items()) for a in c.attendee
                                 ) if c.attendee else 'None'
        str_organizer = shorten(str_organizer, 255)
        str_attendee = shorten(str_attendee, 255)

        conf_in_db = await YandexConference.get_conference(conn, c.uid)

        # if added conf
        if not conf_in_db:
            await YandexConference.add_conference(
                conn,
                cal_id=cal_id,
                uid=c.uid,
                timezone=c.timezone,
                dtstart=c.dtstart,
                dtend=c.dtend,
                summary=c.summary,
                created=c.created,
                last_modified=c.last_modified,
                description=c.description,
                url_event=c.url_event,
                categories=c.categories,
                x_telemost_conference=c.x_telemost_conference,
                organizer=str_organizer,
                attendee=str_attendee,
                location=c.location,
            )

            if notify is True:
                new_table = create_conference_table(c)
                represents = await notification_views.notify_loaded_conference_view(
                    "loaded_conference.md", calendar_name, "added", None, new_table
                )

                asyncio.create_task(send_msg_client(mm_user_id, represents.get('text')))
        # if updated conf
        elif not equal_conferences(c, conf_in_db):
            await YandexConference.update_conference(
                conn,
                uid=c.uid,
                timezone=c.timezone,
                dtstart=c.dtstart,
                dtend=c.dtend,
                summary=c.summary,
                created=c.created,
                last_modified=c.last_modified,
                description=c.description,
                url_event=c.url_event,
                categories=c.categories,
                x_telemost_conference=c.x_telemost_conference,
                organizer=str_organizer,
                attendee=str_attendee,
                location=c.location,
            )

            if notify is True:
                was_table = create_row_table(conf_in_db)
                new_table = create_conference_table(c)

                represents = await notification_views.notify_loaded_conference_view(
                    "loaded_conference.md", calendar_name, "updated", was_table, new_table
                )

                asyncio.create_task(send_msg_client(mm_user_id, represents.get('text')))

        else:

            continue

        # if conference was passed then skip
        if past_conference(c) or conference_all_day(c):
            continue

        # new conference + user e_c or ch_stat + start date > now + 15 min
        if Conf.TESTING:
            if (user.e_c or user.ch_stat) and caldav_filters.start_gt_now(c.dtstart):  # debug
                start_job = get_dt_with_UTC_tz_from_iso(c.dtstart) - timedelta(seconds=10)  # debug

                delay = get_delay_with_dtstart(start_job)
                task2.send_with_options(args=(user.session, c.uid, c.dtstart), delay=delay)

        else:
            if (user.e_c or user.ch_stat) and caldav_filters.start_gt_15_min(c.dtstart):  # production
                start_job = get_dt_with_UTC_tz_from_iso(c.dtstart) - timedelta(minutes=10)  # production

                delay = get_delay_with_dtstart(start_job)
                task2.send_with_options(args=(user.session, c.uid, c.dtstart), delay=delay)

    async for conf in YandexConference.get_conferences_by_cal_id(conn, cal_id):
        if conf.uid not in conf_uids:

            await YandexConference.remove_conference(conn, conf.uid)

            if notify is True:
                was_table = create_row_table(conf)

                represents = await notification_views.notify_loaded_conference_view(
                    'loaded_conference.md', calendar_name, 'deleted', was_table, None
                )

                asyncio.create_task(send_msg_client(mm_user_id, represents.get('text')))
