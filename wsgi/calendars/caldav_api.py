from wsgi.calendars import calendar_views, caldav_searchers
from wsgi.errors import ClientError
from wsgi.notifications import notification_views

import logging, traceback, requests, caldav
from flask import Request
from caldav import Principal, Calendar
from datetime import datetime, timedelta, UTC
from zoneinfo import ZoneInfo
from sqlalchemy.engine import Row


def take_principal(user: Row) -> Principal | dict:
    user_id, login, token = user.user_id, user.login, user.token

    url = f'https://{login}:{token}@caldav.yandex.ru'

    try:

        with caldav.DAVClient(url=url) as client:
            principal = client.principal()

    except caldav.lib.error.AuthorizationError as exp:

        principal = {
            'type': 'error',
            'text': 'Incorrect username or token. Possible, you changed the username and password'
        }

    except requests.RequestException as exp:

        principal = {
            'type': 'error',
            'text': 'Yandex Calendar server error',
        }

        logging.error('Exception: %s; Traceback: ```%s```' % (exp, traceback.format_exc()))

    except Exception as exp:

        principal = {
            'type': 'error',
            'text': 'Another error'
        }

        logging.error('Exception: %s; Traceback: ```%s```' % (exp, traceback.format_exc()))

    return principal


def get_a_week(user: Row) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    start = datetime.now(UTC).astimezone(tz=ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start + timedelta(days=7)

    return calendar_views.base_view(principal.calendars(), 'get_all.md', [start, end])


def get_a_month(user: Row) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    start = datetime.now(UTC).astimezone(tz=ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start + timedelta(days=30)

    return calendar_views.base_view(principal.calendars(), 'get_all.md', [start, end])


def from_to(user: Row, request: Request) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    dtstart, dtend = request.json['values']['from_date'], request.json['values']['to_date']

    try:

        start = (datetime.strptime(dtstart, '%d.%m.%Y')
                 .replace(tzinfo=ZoneInfo(user.timezone)))
        end = (datetime.strptime(dtend, '%d.%m.%Y')
               .replace(tzinfo=ZoneInfo(user.timezone), hour=23, minute=59, second=59))

    except ClientError as exp:

        return {
            'type': 'error',
            'text': f'Wrong format from date and to date: {dtstart}, {dtend}'
        }

    else:

        if start > end:
            start, end = end, start

        return calendar_views.base_view(principal.calendars(), 'get_all.md', [start, end])


def current(user: Row, request: Request) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    dt = request.json['values']['date']

    try:

        start = datetime.strptime(dt, '%d.%m.%Y').replace(tzinfo=ZoneInfo(user.timezone))
        end = start.replace(hour=23, minute=59, second=59)

    except ClientError as exp:

        return {
            'type': 'error',
            'text': f'Wrong format date. -> {dt}'
        }

    else:

        return calendar_views.base_view(principal.calendars(), 'get_all.md', [start, end])


def today(user: Row) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    start = datetime.now(UTC).astimezone(tz=ZoneInfo(user.timezone))
    end = start.replace(hour=23, minute=59, second=59)

    return calendar_views.base_view(principal.calendars(), 'get_all.md', [start, end])


def daily_notification(user: Row, calendar_name: str) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    try:

        cal = principal.calendar(name=calendar_name)

    except caldav.lib.error.NotFoundError as exp:

        return {
            'type': 'error',
            'text': 'You don\'t have a calendar with this name {}. You need create notify with exists calendars'
            .format(calendar_name)
        }

    start = datetime.now(UTC).astimezone(tz=ZoneInfo(user.timezone))
    end = start.replace(hour=23, minute=59, second=59)

    return notification_views.daily_notify_view(cal, 'get_daily.md', [start, end])


def first_conference_notification(user, calendar_name: str) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    try:

        cal = principal.calendar(name=calendar_name)

    except caldav.lib.error.NotFoundError as exp:

        return {
            'type': 'error',
            'text': 'You don\'t have a calendar with this name {}. You need create notify with exists calendars'
            .format(calendar_name)
        }

    logging.critical(f'user timezone={user.timezone}')
    start = datetime.now(UTC).astimezone(ZoneInfo(user.timezone))
    end = start + timedelta(days=365)

    return notification_views.first_conference_view(cal, 'first_conference.md', [start, end])


def exist_conferences_view(c: Calendar):
    start = datetime.now(UTC)
    end = start + timedelta(days=365 * 4)

    return caldav_searchers.find_first_conferences(c, [start, end])
