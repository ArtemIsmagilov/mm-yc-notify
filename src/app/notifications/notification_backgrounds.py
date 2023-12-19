from secrets import token_hex
from caldav import Principal
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import caldav.lib.error as caldav_errs

from settings import Conf
from .. import dict_responses
from ..async_wraps.async_wrap_caldav import caldav_calendar_by_cal_id
from ..calendars.caldav_searchers import find_conferences_in_one_cal
from ..converters import get_h_m_utc, get_delay_daily
from ..decorators.account_decorators import app_error
from ..notifications import tasks
from ..schemas import UserView
from ..sql_app.crud import User, YandexCalendar
from ..sql_app.database import get_conn


@app_error
async def bg_continue_create_notification(
        user: UserView,
        principal: Principal,
        cals_form: list,
        daily_clock: str,
        e_c: bool,
        ch_stat: bool,
):
    h, m = get_h_m_utc(daily_clock, user.timezone)

    result_cals_cal_id = await asyncio.gather(*(
        asyncio.create_task(caldav_calendar_by_cal_id(principal, cal_id=c['value'])) for c in cals_form
    ))

    dt_start = datetime.now(ZoneInfo(user.timezone)).replace(microsecond=0)
    dt_end = dt_start + timedelta(days=Conf.RANGE_DAYS)

    try:
        result_cals_confs = await asyncio.gather(*(
            asyncio.create_task(find_conferences_in_one_cal(result_cal, (dt_start, dt_end)))
            for result_cal in result_cals_cal_id
        ))

    except caldav_errs.NotFoundError as exp:

        return dict_responses.calendar_not_found()

    sync_cals_in_db = [{'mm_user_id': user.mm_user_id, 'cal_id': sync_cal.id} for sync_cal in result_cals_cal_id]

    async with get_conn() as conn:
        session = token_hex(16)
        await User.update_user(conn, user.mm_user_id, e_c=e_c, ch_stat=ch_stat, session=session)
        await YandexCalendar.add_many_cals(conn, sync_cals_in_db)

        user.e_c, user.ch_stat, user.session = e_c, ch_stat, session
        for cal_confs in result_cals_confs:
            await tasks.load_updated_added_deleted_events(conn, user, cal_confs, notify=False)


    delay = get_delay_daily(h, m)
    tasks.task1.send_with_options(args=(user.session, h, m), delay=delay)


@app_error
async def bg_continue_update_notification(
        user: UserView,
        principal: Principal,
        cals_form: list,
        daily_clock: str,
        e_c: bool,
        ch_stat: bool,
):
    async with get_conn() as conn:
        await YandexCalendar.remove_cals(conn, user.mm_user_id)
    asyncio.create_task(bg_continue_create_notification(user, principal, cals_form, daily_clock, e_c, ch_stat))


@app_error
async def bg_remove_notification(
        mm_user_id: str
):
    async with get_conn() as conn:
        await YandexCalendar.remove_cals(conn, mm_user_id)
        await User.update_user(conn, mm_user_id, e_c=False, ch_stat=False, session=token_hex(16))

