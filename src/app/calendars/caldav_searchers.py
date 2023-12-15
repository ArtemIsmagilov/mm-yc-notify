from ..async_wraps.async_wrap_caldav import caldav_search
from ..calendars.conference import Conference

from datetime import datetime
from caldav import Calendar, Event
import asyncio
from typing import AsyncGenerator, Sequence, Generator


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
    events = await caldav_search(cal, event=True, start=dates[0], end=dates[1], sort_keys=('dtstart',))

    conferences = [i for i in event_filter(events, dates[0], dates[1])]

    if conferences:
        return cal, conferences


def event_filter(events: list[Event], dtstart: datetime, dtend: datetime) -> Generator[Conference, None, None]:
    for e in events:
        icalendar_component = e.icalendar_component
        if icalendar_component.get("X-TELEMOST-CONFERENCE"):
            tz = str(dtstart.tzinfo)
            conf = Conference(icalendar_component, tz)
            if dtstart <= datetime.fromisoformat(conf.dtstart) and dtend >= datetime.fromisoformat(conf.dtend):
                yield conf
