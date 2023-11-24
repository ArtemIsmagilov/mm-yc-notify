from ..calendars import caldav_searchers

from datetime import datetime
from quart import render_template


async def base_view(calendars: tuple | dict, template: str, dates: tuple[datetime, datetime]) -> dict:
    if type(calendars) is dict:
        return calendars

    represents = [r async for r in caldav_searchers.find_conferences_in_some_cals(calendars, dates)]

    if not represents:
        return {
            'type': 'ok',
            'text': 'No conferences',
        }

    return {
        'type': 'ok',
        'text': await render_template(template, represents=represents)
    }
