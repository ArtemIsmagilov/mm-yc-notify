from wsgi.calendars import caldav_searchers
from wsgi.calendars.conference import Conference
from datetime import datetime

from caldav import Calendar
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader("wsgi"), autoescape=select_autoescape())


def daily_notify_view(calendars: list[Calendar, ...], template: str, dates: tuple[datetime, datetime]) -> dict:
    represents = caldav_searchers.find_conferences_in_some_cals(calendars, dates)

    tm = env.get_template(template)

    if not represents:

        return {
            'type': 'ok',
            'text': 'Today you don\'t have conferences',
        }

    return {
        'type': 'ok',
        'text': tm.render(represents=represents),
    }


def notify_next_conference_view(template: str, calendar_name: str, conf_obj: Conference):
    tm = env.get_template(template)
    text = tm.render(calendar_name=calendar_name, c=conf_obj)

    return {
        'type': 'ok',
        'text': text,
    }


def notify_loaded_conference_view(template: str, calendar_name: str, loaded: str, was_table: dict, now_table: dict):
    tm = env.get_template(template)
    text = tm.render(calendar_name=calendar_name, was_table=was_table, now_table=now_table, loaded=loaded)

    return {
        'type': 'ok',
        'text': text,
    }