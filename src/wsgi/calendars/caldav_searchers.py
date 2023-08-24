from wsgi.calendars.conference import Conference

from datetime import datetime
from caldav import Calendar


def find_conferences_in_some_cals(calendars: list[Calendar], dates: tuple[datetime, datetime]) -> list[(str, list[Conference, ...]), ...]:
    result = []

    timezone = str(dates[0].tzinfo)

    for cal in calendars:
        events = cal.search(start=dates[0], end=dates[1], event=True, sort_keys=("dtstart",))


        conferences = [
            Conference(e.icalendar_component, timezone) for e in events
            if e.icalendar_component.get("X-TELEMOST-CONFERENCE")
        ]

        if conferences:
            result.append((cal.get_display_name(), conferences))

    return result


def find_conferences_in_one_cal(cal: Calendar, dates: tuple[datetime, datetime]) -> list[Conference, ...]:
    events = cal.search(start=dates[0], end=dates[1], event=True, sort_keys=("dtstart",))

    timezone = str(dates[0].tzinfo)

    conferences = [
        Conference(e.icalendar_component, timezone) for e in events
        if e.icalendar_component.get("X-TELEMOST-CONFERENCE")
    ]

    return conferences
