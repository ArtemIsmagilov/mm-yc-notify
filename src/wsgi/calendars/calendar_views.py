from wsgi.calendars import caldav_searchers

from datetime import datetime
from flask import render_template


def base_view(calendars: list, template: str, dates: list[datetime, datetime]):
    represents = caldav_searchers.find_conferences(calendars, dates)

    if not represents:

        return {
            'type': 'ok', 'text': 'No conferences',
        }

    return {
        'type': 'ok',
        'text': render_template(template, represents=represents)
    }
