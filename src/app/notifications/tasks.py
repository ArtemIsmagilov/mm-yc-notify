import asyncio, json, logging
from dramatiq import actor
from textwrap import shorten
from datetime import timedelta, datetime, UTC
import caldav.lib.error as caldav_errors
from caldav import Principal, Calendar
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncConnection
from typing import Sequence, Generator
from ..app_handlers import static_file
from ..async_wraps.async_wrap_caldav import (
    caldav_calendar_by_cal_id, caldav_event_by_uid, caldav_get_supported_components
)
from ..bots.bot_commands import send_msg_client, update_custom_status, get_user_by_mm_user_id
from ..calendars import caldav_api, caldav_filters
from ..calendars.caldav_funcs import take_principal
from ..calendars.caldav_searchers import find_conferences_in_one_cal
from ..calendars.conference import Conference
from ..converters import (
    get_dt_with_UTC_tz_from_iso, iso1_gt_iso2, dont_clear, create_conference_table, create_row_table, equal_conferences,
    get_delay_with_dtstart, get_delay_daily, conference_all_day, past_conference, to_str_organizer, to_str_attendee
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
async def task2(session: str, conf_id: str, dtstart: str):
    """notify_next_conference_job"""
    logging.debug('notify_next_conference_job(%s, %s, %s)', session, conf_id, dtstart)
    await notify_next_conference_job(session, conf_id, dtstart)


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

    dt_start = datetime.now(ZoneInfo(user.timezone)).replace(microsecond=0)
    dt_end = dt_start + timedelta(days=Conf.RANGE_DAYS)

    try:
        cal_confs = await find_conferences_in_one_cal(cal_in_server, (dt_start, dt_end))

    except caldav_errors.NotFoundError as exp:
        await YandexCalendar.remove_cal(conn, user_cal_in_db.cal_id)

    else:
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


async def notify_next_conference_job(session: str, conf_id: str, dtstart: str) -> None:
    async with get_conn() as conn:
        user = await User.get_user_by_session(conn, session)

        if not user:
            return

        principal = await take_principal(user.login, user.token)

        if type(principal) is dict:
            await User.remove_user(conn, user.mm_user_id)

            return

        conf_in_db = await YandexConference.get_conference(conn, conf_id)

        if not conf_in_db:
            return

        cal = await caldav_calendar_by_cal_id(principal, cal_id=conf_in_db.cal_id)

        try:

            await caldav_get_supported_components(cal)

        except caldav_errors.NotFoundError as exp:

            await YandexCalendar.remove_cal(conn, cal.id)

        try:

            event = await caldav_event_by_uid(cal, uid=conf_in_db.uid)

        except caldav_errors.NotFoundError as exp:

            await YandexConference.remove_conferences_by_uid(conn, uid=conf_in_db.uid)

            return

        i_event = event.icalendar_instance.subcomponents[-1]

        if i_event.get('X-TELEMOST-CONFERENCE'):

            # if conference.dtstart has modified than skip send email
            if datetime.fromisoformat(dtstart) != conf_in_db.dtstart:
                return

            if caldav_filters.is_exist_conf_at_time(conf_in_db.dtstart):
                if user.e_c:
                    pretext = 'Upcoming conference!'
                    msg = '### Bot send notification!'

                    represents = await notification_views.notify_next_conference_view(
                        'first_conference.md', str(cal), Conference(i_event, user.timezone)
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
                    delay = get_delay_with_dtstart(conf_in_db.dtstart)

                    task3.send_with_options(args=(session, conf_in_db.dtend.isoformat()), delay=delay)


async def daily_notification_job(session: str, hour: int, minute: int):
    async with get_conn() as conn:
        user = await User.get_user_by_session(conn, session)

        if not user:
            return

        principal = await take_principal(user.login, user.token)

        if type(principal) is dict:
            await User.remove_user(conn, user.mm_user_id)
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
        cal_confs: tuple[Calendar, Generator[Conference, None, None]] | None,
        notify=True
):
    cal, confs = cal_confs
    mm_user_id = user.mm_user_id
    cal_id = cal.id
    calendar_name = str(cal)
    conf_ids = set()
    dt_now = datetime.now(UTC).replace(microsecond=0)

    for ld_c in confs:
        conf_ids.add(ld_c.conf_id)

        organizer = shorten(to_str_organizer(ld_c.organizer), 255) if ld_c.organizer else None
        attendee = shorten(to_str_attendee(ld_c.attendee), 255) if ld_c.attendee else None

        conf_in_db = await YandexConference.get_conference(conn, ld_c.conf_id)

        # if added conf
        if not conf_in_db:

            recurrence_conf = await YandexConference.get_first_conference_by_uid(conn, ld_c.uid) if ld_c.recurrence_id else None

            await YandexConference.add_conference(
                conn,
                conf_id=ld_c.conf_id,
                cal_id=cal_id,
                uid=ld_c.uid,
                timezone=ld_c.timezone,
                dtstart=ld_c.dtstart,
                dtend=ld_c.dtend,
                summary=ld_c.summary,
                created=ld_c.created,
                last_modified=ld_c.last_modified,
                description=ld_c.description,
                url_event=ld_c.url_event,
                categories=ld_c.categories,
                x_telemost_conference=ld_c.x_telemost_conference,
                organizer=organizer,
                attendee=attendee,
                location=ld_c.location,
                recurrence_id=ld_c.recurrence_id,
            )

            if notify is True and (not ld_c.recurrence_id or not recurrence_conf) and ld_c.created + timedelta(minutes=30) >= dt_now:
                new_table = create_conference_table(ld_c)
                represents = await notification_views.notify_loaded_conference_view(
                    "loaded_conference.md", calendar_name, "added", None, new_table
                )

                asyncio.create_task(send_msg_client(mm_user_id, represents.get('text')))

        # if updated conf
        elif not equal_conferences(ld_c, conf_in_db):

            recurrence_conf = await YandexConference.get_first_conference_by_uid(conn, ld_c.uid) if ld_c.recurrence_id else None

            await YandexConference.update_conference(
                conn,
                conf_id=ld_c.conf_id,
                uid=ld_c.uid,
                timezone=ld_c.timezone,
                dtstart=ld_c.dtstart,
                dtend=ld_c.dtend,
                summary=ld_c.summary,
                created=ld_c.created,
                last_modified=ld_c.last_modified,
                description=ld_c.description,
                url_event=ld_c.url_event,
                categories=ld_c.categories,
                x_telemost_conference=ld_c.x_telemost_conference,
                organizer=organizer,
                attendee=attendee,
                location=ld_c.location,
                recurrence_id=ld_c.recurrence_id,
            )

            if notify is True and (not ld_c.recurrence_id or not recurrence_conf):
                was_table = create_row_table(conf_in_db, user.timezone)
                new_table = create_conference_table(ld_c)

                represents = await notification_views.notify_loaded_conference_view(
                    "loaded_conference.md", calendar_name, "updated", was_table, new_table
                )

                asyncio.create_task(send_msg_client(mm_user_id, represents.get('text')))

        else:

            continue

        # if conference was passed or all day or not updated dtstart then skip
        if past_conference(ld_c) or conference_all_day(ld_c) or (conf_in_db and conf_in_db.dtstart == ld_c.dtstart):
            continue

        # new conference + user e_c or ch_stat + start date > now + 15 min
        if Conf.TESTING:
            # debug
            if (user.e_c or user.ch_stat) and caldav_filters.start_gt_now(ld_c.dtstart):
                start_job = get_dt_with_UTC_tz_from_iso(ld_c.dtstart) - timedelta(seconds=10)

                delay = get_delay_with_dtstart(start_job)
                task2.send_with_options(args=(user.session, ld_c.conf_id, str(ld_c.dtstart)), delay=delay)

        else:
            # production
            if (user.e_c or user.ch_stat) and caldav_filters.start_gt_10_min(ld_c.dtstart):
                start_job = get_dt_with_UTC_tz_from_iso(ld_c.dtstart) - timedelta(minutes=10)

                delay = get_delay_with_dtstart(start_job)
                task2.send_with_options(args=(user.session, ld_c.conf_id, str(ld_c.dtstart)), delay=delay)

    # if removed conf
    if not conf_ids:
        return

    rm_cs = {}
    async for rm_c in YandexConference.remove_conferences_not_in_confs_uid_by_cal_id(conn, cal_id, conf_ids):
        if notify and rm_c.dtend > dt_now:
            recurrence_conf = await YandexConference.get_first_conference_by_uid(conn, rm_c.uid) if rm_c.recurrence_id else None
            if not rm_c.recurrence_id or not recurrence_conf:
                rm_cs[rm_c.uid] = rm_c

    for c_uid in rm_cs:
        was_table = create_row_table(rm_cs[c_uid], user.timezone)

        represents = await notification_views.notify_loaded_conference_view(
            'loaded_conference.md', calendar_name, 'deleted', was_table, None
        )

        asyncio.create_task(send_msg_client(mm_user_id, represents.get('text')))
