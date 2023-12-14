from ..async_wraps.async_wrap_caldav import caldav_search
from ..calendars.conference import Conference

from datetime import datetime
from caldav import Calendar
import asyncio
from typing import AsyncGenerator, Sequence


async def find_conferences_in_some_cals(
        calendars: Sequence[Calendar],
        dates: tuple[datetime, datetime],
) -> AsyncGenerator[Sequence[Conference], None] | None:
    tasks_generator = (asyncio.create_task(find_conferences_in_one_cal(cal, dates)) for cal in calendars)

    for task in asyncio.as_completed(tasks_generator):
        earliest_result = await task
        if earliest_result:
            yield earliest_result


async def find_conferences_in_one_cal(
        cal: Calendar,
        dates: tuple[datetime, datetime],
) -> tuple[Calendar, Sequence[Conference]] | None:
    tz = str(dates[0].tzinfo)
    events = await caldav_search(cal, event=True, start=dates[0], end=dates[1], sort_keys=('dtstart',))

    conferences = [
        Conference(e.icalendar_component, tz) for e in events if e.icalendar_component.get("X-TELEMOST-CONFERENCE")
    ]

    if conferences:
        return cal, conferences
