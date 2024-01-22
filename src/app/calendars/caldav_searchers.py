import asyncio
from typing import (
    AsyncGenerator,
    Sequence,
    Generator
)
from datetime import datetime

from caldav import (
    Calendar,
    Event
)

from ..async_wraps.async_wrap_caldav import caldav_search
from ..calendars.conference import Conference


async def find_conferences_in_some_cals(
        calendars: Sequence[Calendar],
        dates: tuple[datetime, datetime],
) -> AsyncGenerator[Generator[Conference, None, None], None]:
    tasks_generator = (find_conferences_in_one_cal(cal, dates) for cal in calendars)

    for task in asyncio.as_completed(tasks_generator):
        yield await task


async def find_conferences_in_one_cal(
        cal: Calendar,
        dates: tuple[datetime, datetime],
) -> tuple[Calendar, Generator[Conference, None, None]]:
    events = await caldav_search(cal, start=dates[0], end=dates[1], event=True, expand=True, sort_keys=['dtstart'])

    conferences = event_filter(events, dates[0], dates[1])

    return cal, conferences


def event_filter(events: list[Event], dtstart: datetime, dtend: datetime) -> Generator[Conference, None, None]:
    for e in events:
        icalendar_component = e.icalendar_instance.subcomponents[-1]
        if icalendar_component.get("X-TELEMOST-CONFERENCE"):
            conf = Conference(icalendar_component, str(dtstart.tzinfo))
            if dtstart <= conf.dtstart and dtend >= conf.dtend:
                yield conf
