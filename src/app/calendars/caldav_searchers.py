from ..calendars.conference import Conference

from datetime import datetime
from caldav import Calendar
import asyncio
from typing import AsyncGenerator


async def find_conferences_in_some_cals(
        calendars: list[Calendar] | tuple[Calendar],
        dates: tuple[datetime, datetime],
) -> AsyncGenerator[list[Conference], None]:
    tasks_generator = (asyncio.create_task(find_conferences_in_one_cal(cal, dates)) for cal in calendars)

    for task in asyncio.as_completed(tasks_generator):
        earliest_result = await task
        if earliest_result:
            yield earliest_result


async def find_conferences_in_one_cal(
        cal: Calendar,
        dates: tuple[datetime, datetime],
) -> tuple[str | None, list[Conference]]:
    timezone = str(dates[0].tzinfo)
    events = await asyncio.to_thread(cal.search, start=dates[0], end=dates[1], event=True, sort_keys=("dtstart",))
    conferences = [
        Conference(e.icalendar_component, timezone) for e in events
        if e.icalendar_component.get("X-TELEMOST-CONFERENCE")
    ]

    if conferences:
        return str(cal), conferences
