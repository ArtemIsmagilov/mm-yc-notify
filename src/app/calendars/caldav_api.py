from sqlalchemy.ext.asyncio import AsyncConnection

from ..calendars import calendar_views
from ..decorators.account_decorators import dependency_principal, auth_required
from .. import dict_responses
from ..notifications import notification_views

from quart import request
from caldav import Principal, Calendar
import caldav.lib.error as caldav_errs
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.engine import Row
import asyncio
from typing import AsyncGenerator


@auth_required
@dependency_principal
async def get_a_week(
        conn: AsyncConnection,
        user: Row,
        principal: Principal,
) -> dict:
    start = datetime.now(ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start + timedelta(days=7)

    cals = await get_all_calendars(principal)

    return await calendar_views.base_view(cals, 'get_all.md', (start, end))


@auth_required
@dependency_principal
async def get_a_month(
        conn: AsyncConnection,
        user: Row,
        principal: Principal,
) -> dict:
    start = datetime.now(ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start + timedelta(days=30)

    cals = await get_all_calendars(principal)

    return await calendar_views.base_view(cals, 'get_all.md', (start, end))


@auth_required
@dependency_principal
async def from_to(
        conn: AsyncConnection,
        user: Row,
        principal: Principal,
) -> dict:
    data = await request.json

    mm_username = data['context']['acting_user']['username']
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

        cals = await get_all_calendars(principal)

        return await calendar_views.base_view(cals, 'get_all.md', (start, end))


@auth_required
@dependency_principal
async def current(
        conn: AsyncConnection,
        user: Row,
        principal: Principal,
) -> dict:
    data = await request.json

    mm_username = data['context']['acting_user']['username']
    dt = data['values']['date']

    try:

        start = datetime.strptime(dt, '%d.%m.%Y').replace(tzinfo=ZoneInfo(user.timezone))
        end = start.replace(hour=23, minute=59, second=59)

    except ValueError as exp:

        return dict_responses.wrong_format_date_current(mm_username, dt)

    else:

        cals = await get_all_calendars(principal)

        return await calendar_views.base_view(cals, 'get_all.md', (start, end))


@auth_required
@dependency_principal
async def today(
        conn: AsyncConnection,
        user: Row,
        principal: Principal,
) -> dict:
    start = datetime.now(ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start.replace(hour=23, minute=59, second=59)

    cals = await get_all_calendars(principal)

    return await calendar_views.base_view(cals, 'get_all.md', (start, end))


async def daily_notification(
        principal: Principal,
        user: Row,
        exist_calendars: list[Calendar]
) -> dict:
    start = datetime.now(ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start.replace(hour=23, minute=59, second=59)

    return await notification_views.daily_notify_view(exist_calendars, 'get_daily.md', (start, end))


async def get_all_calendars(principal: Principal) -> list[Calendar] | dict:
    result = await asyncio.to_thread(principal.calendars)
    if not result:
        return dict_responses.no_calendars_on_server()
    return result


async def get_calendar_by_name(principal: Principal, name: str) -> Calendar | dict:
    try:
        result = await asyncio.to_thread(principal.calendar, name=name)
    except caldav_errs.NotFoundError as exp:
        return dict_responses.calendar_dosnt_exists()
    return result


async def create_calendar(principal: Principal, *args, **kwargs):
    return await asyncio.to_thread(principal.make_calendar, *args, **kwargs)


async def check_exist_calendars_by_cal_id(
        principal: Principal,
        cals: AsyncGenerator[Row, None],
) -> list[Calendar] | dict:
    tasks_cals_generator = [
        asyncio.create_task(asyncio.to_thread(principal.calendar, cal_id=c.cal_id)) async for c in cals
    ]

    async with asyncio.TaskGroup() as tg:
        tasks_cals = set()
        for task in asyncio.as_completed(tasks_cals_generator):
            cal = await task
            try:

                tasks_cals.add(tg.create_task(asyncio.to_thread(cal.objects_by_sync_token)))

            except caldav_errs.NotFoundError as exp:

                return dict_responses.calendar_dosnt_exists()

    result = [task.result().calendar for task in tasks_cals]

    if not result:
        return dict_responses.no_calendars_on_server()

    return result
