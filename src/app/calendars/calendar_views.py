from datetime import datetime
from quart import render_template
from typing import Sequence
from caldav import Calendar

from ..calendars import caldav_searchers
from ..constants import CONFERENCE_PROPERTIES


async def base_view(calendars: Sequence[Calendar] | dict, template: str, dates: tuple[datetime, datetime]) -> dict:
    if type(calendars) is dict:
        return calendars

    represents = caldav_searchers.find_conferences_in_some_cals(calendars, dates)

    return {
        'type': 'ok',
        'text': await render_template(template, represents=represents)
    }
