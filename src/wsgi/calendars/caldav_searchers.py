from wsgi.calendars.conference import Conference

from datetime import datetime
from caldav import Calendar


def find_conferences(calendars: list[Calendar], dates: list[datetime, datetime]) -> list[Conference]:
    result = []

    timezone = str(dates[0].tzinfo)

    for cal in calendars:

        events = cal.search(start=dates[0], end=dates[1], event=True, expand=True, sort_keys=['dtstart'])

        if events:

            result.append((cal.name, []))

            for e in events:

                ievent = e.icalendar_component

                if ievent.get('X-TELEMOST-CONFERENCE'):
                    result[-1][-1].append(Conference(ievent, timezone))

            if not result[-1][-1]:
                result.pop(-1)

    return result


def find_conferences_today(cal: Calendar, dates: list[datetime, datetime]) -> list[Conference]:
    conferences = []

    events = cal.search(start=dates[0], end=dates[1], event=True, expand=True, sort_keys=['dtstart'])

    timezone = str(dates[0].tzinfo)

    for e in events:

        ievent = e.icalendar_component

        if ievent.get('X-TELEMOST-CONFERENCE'):
            conferences.append(Conference(ievent, timezone))

    return conferences


def find_first_conferences(cal: Calendar, dates: list[datetime, datetime]) -> list[Conference, ...]:
    conferences = []

    events = cal.search(start=dates[0], end=dates[1], event=True, expand=True, sort_keys=['dtstart'])

    timezone = str(dates[0].tzinfo)

    for e in events:

        ievent = e.icalendar_component

        if ievent.get('X-TELEMOST-CONFERENCE'):
            conference = Conference(ievent, timezone)

            conferences.append(conference)

    return conferences
