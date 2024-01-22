import asyncio

from caldav import (
    Principal,
    Calendar,
    DAVClient,
    CalendarObjectResource
)
import caldav.lib.error as caldav_errs

from .. import dict_responses


async def caldav_all_calendars(principal: Principal) -> list[Calendar] | dict:
    result = await asyncio.to_thread(principal.calendars)
    if not result:
        return dict_responses.no_calendars_on_server()
    return result


async def caldav_calendar_by_name(principal: Principal, name: str) -> Calendar | dict:
    try:
        result = await asyncio.to_thread(principal.calendar, name=name)
    except caldav_errs.NotFoundError as exp:
        return dict_responses.calendar_dosnt_exists()
    return result


async def caldav_calendar_by_cal_id(principal: Principal, cal_id: str) -> Calendar:
    return await asyncio.to_thread(principal.calendar, cal_id=cal_id)


async def caldav_search(calendar: Calendar, *args, **kwargs) -> list[CalendarObjectResource]:
    return await asyncio.to_thread(calendar.search, *args, **kwargs)


async def caldav_event_by_uid(calendar: Calendar, *args, **kwargs) -> CalendarObjectResource:
    return await asyncio.to_thread(calendar.event_by_uid, *args, **kwargs)


async def caldav_principal(client: DAVClient) -> Principal:
    return await asyncio.to_thread(client.principal)


async def caldav_create_calendar(principal: Principal, *args, **kwargs) -> Calendar:
    return await asyncio.to_thread(principal.make_calendar, *args, **kwargs)


async def caldav_get_supported_components(calendar: Calendar):
    return await asyncio.to_thread(calendar.get_supported_components)
