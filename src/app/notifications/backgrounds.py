from sqlalchemy.engine import Row
from caldav import Principal
import asyncio
import caldav.lib.error as caldav_errs

from .. import dict_responses
from ..calendars.caldav_api import get_calendar_by_cal_id
from ..converters import get_h_m_utc, get_delay_daily
from ..notifications import tasks
from ..sql_app.crud import User, YandexCalendar
from ..sql_app.database import get_conn


async def bg_continue_create_notification(
        user: Row,
        principal: Principal,
        cals_form: list,
        daily_clock: str,
        e_c: bool,
        ch_stat: bool,
):
    h, m = get_h_m_utc(daily_clock, user.timezone)

    async with asyncio.TaskGroup() as tg:
        result_cals_cal_id = set(
            tg.create_task(get_calendar_by_cal_id(principal, cal_id=c['value'])) for c in cals_form)

    try:
        async with asyncio.TaskGroup() as tg:
            result_sync_cals = set(
                tg.create_task(asyncio.to_thread(result_cal.result().objects_by_sync_token, load_objects=True))
                for result_cal in result_cals_cal_id
            )

    except caldav_errs.NotFoundError as exp:

        return dict_responses.calendar_not_found()

    sync_cals_in_db = [
        {'mm_user_id': user.mm_user_id, 'cal_id': sync_cal.result().calendar.id,
         'sync_token': sync_cal.result().sync_token}
        for sync_cal in result_sync_cals
    ]

    async with get_conn() as conn:

        async with asyncio.TaskGroup() as tg:
            tg.create_task(User.update_user(conn, user.mm_user_id, e_c=e_c, ch_stat=ch_stat))

            tg.create_task(YandexCalendar.add_many_cals(conn, sync_cals_in_db))

        async with asyncio.TaskGroup() as tg:
            for sync_cal in result_sync_cals:
                tg.create_task(tasks.load_updated_added_deleted_events(conn, user, sync_cal.result(), notify=False))

    delay = get_delay_daily(h, m)
    tasks.task1.send_with_options(args=(user.mm_user_id, h, m), delay=delay)
