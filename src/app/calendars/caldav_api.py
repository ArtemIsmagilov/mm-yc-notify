from sqlalchemy.ext.asyncio import AsyncConnection

from ..calendars import calendar_views
from ..decorators.account_decorators import dependency_principal, auth_required
from ..errors import ClientError
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
    dtstart, dtend = data['values']['from_date'], data['values']['to_date']

    try:

        start = datetime.strptime(dtstart, '%d.%m.%Y').replace(
            tzinfo=ZoneInfo(user.timezone)
        )
        end = datetime.strptime(dtend, '%d.%m.%Y').replace(
            tzinfo=ZoneInfo(user.timezone), hour=23, minute=59, second=59
        )

    except ClientError as exp:

        return {
            'type': 'error',
            'text': f'Wrong format from date and to date: {dtstart}, {dtend}'
        }

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
    dt = data['values']['date']

    try:

        start = datetime.strptime(dt, '%d.%m.%Y').replace(tzinfo=ZoneInfo(user.timezone))
        end = start.replace(hour=23, minute=59, second=59)

    except ClientError as exp:

        return {
            'type': 'error',
            'text': f'Wrong format date. -> {dt}'
        }

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
        return {
            'type': 'error',
            'text': 'You haven\'t calendars on CalDAV server.'
        }
    return result


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

                return {
                    'type': 'error',
                    'text': f'Calendar doesn\'t exist. Notification scheduler was deleted.',
                }

    result = [task.result().calendar for task in tasks_cals]

    if not result:
        return {
            'type': 'error',
            'text': 'You haven\'t calendars. Notification scheduler was deleted.',
        }

    return result
