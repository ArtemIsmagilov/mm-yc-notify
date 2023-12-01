from sqlalchemy.ext.asyncio import AsyncConnection

from .calendar_backgrounds import run_in_background
from ..async_wraps.async_wrap_caldav import caldav_calendar_by_cal_id, caldav_objects_by_sync_token
from ..decorators.account_decorators import dependency_principal, auth_required
from .. import dict_responses
from ..dict_responses import success_ok
from ..notifications import notification_views

from quart import request
from caldav import Principal, Calendar, SynchronizableCalendarObjectCollection as SyncCal
import caldav.lib.error as caldav_errs
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.engine import Row
import asyncio
from typing import AsyncGenerator, Sequence

from ..schemas import UserView
from ..sql_app.crud import YandexCalendar


@auth_required
@dependency_principal
async def get_a_week(
        conn: AsyncConnection,
        user: UserView,
        principal: Principal,
) -> dict:
    data = await request.json
    mm_username = data['context']['acting_user']['username']
    channel_id = data['context']['channel']['id']
    start = datetime.now(ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start + timedelta(days=7)

    asyncio.create_task(run_in_background(user.mm_user_id, channel_id, principal, start, end))

    return success_ok(mm_username)


@auth_required
@dependency_principal
async def get_a_month(
        conn: AsyncConnection,
        user: UserView,
        principal: Principal,
) -> dict:
    data = await request.json
    mm_username = data['context']['acting_user']['username']
    channel_id = data['context']['channel']['id']
    start = datetime.now(ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start + timedelta(days=30)

    asyncio.create_task(run_in_background(user.mm_user_id, channel_id, principal, start, end))

    return success_ok(mm_username)


@auth_required
@dependency_principal
async def from_to(
        conn: AsyncConnection,
        user: UserView,
        principal: Principal,
) -> dict:
    data = await request.json

    mm_username = data['context']['acting_user']['username']
    channel_id = data['context']['channel']['id']
    dtstart, dtend = data['values']['from_date'], data['values']['to_date']

    try:

        start = datetime.strptime(dtstart, '%d.%m.%Y').replace(
            tzinfo=ZoneInfo(user.timezone)
        )
        end = datetime.strptime(dtend, '%d.%m.%Y').replace(
            tzinfo=ZoneInfo(user.timezone), hour=23, minute=59, second=59
        )

    except ValueError as exp:

        return dict_responses.wrong_format_dates_from_to(mm_username, dtstart, dtend)

    else:

        if start > end:
            start, end = end, start

        asyncio.create_task(run_in_background(user.mm_user_id, channel_id, principal, start, end))

        return success_ok(mm_username)


@auth_required
@dependency_principal
async def current(
        conn: AsyncConnection,
        user: UserView,
        principal: Principal,
) -> dict:
    data = await request.json

    mm_username = data['context']['acting_user']['username']
    channel_id = data['context']['channel']['id']
    dt = data['values']['date']

    try:

        start = datetime.strptime(dt, '%d.%m.%Y').replace(tzinfo=ZoneInfo(user.timezone))
        end = start.replace(hour=23, minute=59, second=59)

    except ValueError as exp:

        return dict_responses.wrong_format_date_current(mm_username, dt)

    else:

        asyncio.create_task(run_in_background(user.mm_user_id, channel_id, principal, start, end))

        return success_ok(mm_username)


@auth_required
@dependency_principal
async def today(
        conn: AsyncConnection,
        user: UserView,
        principal: Principal,
) -> dict:
    data = await request.json
    channel_id = data['context']['channel']['id']
    start = datetime.now(ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start.replace(hour=23, minute=59, second=59)

    asyncio.create_task(run_in_background(user.mm_user_id, channel_id, principal, start, end))

    return success_ok(user.login)


async def daily_notification(
        principal: Principal,
        user: UserView,
        exist_calendars: Sequence[Calendar]
) -> dict:
    start = datetime.now(ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start.replace(hour=23, minute=59, second=59)

    return await notification_views.daily_notify_view(exist_calendars, 'get_daily.md', (start, end))


async def check_exist_calendars_by_cal_id(
        conn: AsyncConnection,
        principal: Principal,
        cals: AsyncGenerator[Row, None],
) -> set[Calendar] | dict:
    background_tasks = [
        asyncio.create_task(caldav_calendar_by_cal_id(principal, cal_id=c.cal_id))
        async for c in cals
    ]

    cals_set = set()
    for task in asyncio.as_completed(background_tasks):
        cal = await task

        try:

            await caldav_objects_by_sync_token(cal)

        except caldav_errs.NotFoundError as exp:

            await YandexCalendar.remove_cal(conn, cal.id)

        else:
            cals_set.add(cal)

    if not cals_set:
        return dict_responses.no_calendars_on_server()

    return cals_set

