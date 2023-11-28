from ..calendars import caldav_searchers
from ..calendars.conference import Conference

from datetime import datetime
from typing import Sequence
from caldav import Calendar
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader('app'), autoescape=select_autoescape(), enable_async=True)


async def daily_notify_view(
        calendars: Sequence[Calendar],
        template: str,
        dates: tuple[datetime, datetime]
) -> dict:
    if not calendars:
        return {
            'type': 'error',
            'text': 'You haven\'t calendars on CalDAV server.'
        }

    represents = [r async for r in caldav_searchers.find_conferences_in_some_cals(calendars, dates)]

    if not represents:
        return {
            'type': 'ok',
            'text': 'Today you don\'t have conferences',
        }

    tm = env.get_template(template)
    text = await tm.render_async(represents=represents)
    return {
        'type': 'ok',
        'text': text,
    }


async def notify_next_conference_view(
        template: str,
        calendar_name: str,
        conf_obj: Conference
):
    tm = env.get_template(template)
    text = await tm.render_async(calendar_name=calendar_name, c=conf_obj)

    return {
        'type': 'ok',
        'text': text,
    }


async def notify_loaded_conference_view(
        template: str,
        calendar_name: str,
        loaded: str,
        was_table: dict,
        now_table: dict
):
    tm = env.get_template(template)
    text = await tm.render_async(calendar_name=calendar_name, was_table=was_table, now_table=now_table, loaded=loaded)

    return {
        'type': 'ok',
        'text': text,
    }
