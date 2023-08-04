from wsgi.calendars import caldav_searchers

from caldav import Calendar
from jinja2 import FileSystemLoader, Environment

env = Environment(loader=FileSystemLoader('wsgi/templates'))


def daily_notify_view(calendar: Calendar, template: str, dates: list):
    conferences = caldav_searchers.find_conferences_today(calendar, dates)

    tm = env.get_template(template)

    if not conferences:
        return {
            'type': 'ok',
            'text': 'Today you don\'t have conferences',
        }

    return {
        'type': 'ok',
        'text': tm.render(calendar_name=calendar.name, conferences=conferences),
    }


def first_conference_view(calendar: Calendar, template: str, dates: list):
    first_conferences = caldav_searchers.find_first_conferences(calendar, dates)

    tm = env.get_template(template)

    if not first_conferences:

        text = 'You don\'t have conferences'

    else:

        text = tm.render(calendar_name=calendar.name, c=first_conferences[0])

    return {
        'type': 'ok',
        'text': text,
        'first_conferences': first_conferences,
        'cal': calendar,
    }



