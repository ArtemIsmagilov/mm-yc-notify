from wsgi.calendars import caldav_searchers

from datetime import datetime
from flask import render_template


def base_view(calendars: list, template: str, dates: tuple[datetime, datetime]) -> dict:
    represents = caldav_searchers.find_conferences_in_some_cals(calendars, dates)

    if not represents:

        return {
            'type': 'ok',
            'text': 'No conferences',
        }

    return {
        'type': 'ok',
        'text': render_template(template, represents=represents)
    }
