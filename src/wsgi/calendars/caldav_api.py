from wsgi.calendars import calendar_views, caldav_searchers
from wsgi.calendars.conference import Conference
from wsgi.errors import ClientError
from wsgi.notifications import notification_views

import logging, traceback, caldav
from flask import Request
from caldav import Principal, Calendar
import caldav.lib.error as caldav_errs
from datetime import datetime, timedelta, UTC
from zoneinfo import ZoneInfo
from sqlalchemy.engine import Row


def take_principal(user: Row) -> Principal | dict:
    mm_user_id, login, token = user.mm_user_id, user.login, user.token

    url = f'https://{login}:{token}@caldav.yandex.ru'

    try:

        with caldav.DAVClient(url=url) as client:
            principal = client.principal()

    except caldav_errs.AuthorizationError as exp:

        principal = {
            'type': 'error',
            'text': 'Incorrect username or token. Possible, you changed the username and password'
        }

    except caldav_errs.DAVError as exp:

        principal = {
            'type': 'error',
            'text': 'Unknown Error. Please, contact with your admin platform.'
        }

        logging.error(
            'Error with mm_user_id=%s. <###traceback###\n%s\n###traceback###>\n\n',
            mm_user_id,
            traceback.format_exc(),
        )

    return principal


def get_a_week(user: Row) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    start = datetime.now(UTC).astimezone(tz=ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start + timedelta(days=7)

    return calendar_views.base_view(principal.calendars(), 'get_all.md', (start, end))


def get_a_month(user: Row) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    start = datetime.now(UTC).astimezone(tz=ZoneInfo(user.timezone)).replace(hour=0, minute=0, second=0)
    end = start + timedelta(days=30)

    return calendar_views.base_view(principal.calendars(), 'get_all.md', (start, end))


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

        return calendar_views.base_view(principal.calendars(), 'get_all.md', (start, end))


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

        return calendar_views.base_view(principal.calendars(), 'get_all.md', (start, end))


def today(user: Row) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    start = datetime.now(UTC).astimezone(tz=ZoneInfo(user.timezone))
    end = start.replace(hour=23, minute=59, second=59)

    return calendar_views.base_view(principal.calendars(), 'get_all.md', (start, end))


def daily_notification(user: Row, exist_calendars: list[Calendar, ...]) -> dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    start = datetime.now(UTC).astimezone(tz=ZoneInfo(user.timezone))
    end = start.replace(hour=23, minute=59, second=59)

    return notification_views.daily_notify_view(exist_calendars, 'get_daily.md', (start, end))


def get_cals_with_confs(user: Row) -> dict | list[Calendar, ...]:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    start = datetime.now(UTC).astimezone(ZoneInfo(user.timezone))
    end = start + timedelta(days=365)

    return [c for c in principal.calendars() if caldav_searchers.find_conferences_in_one_cal(c, (start, end))]


def get_all_cals(user: Row):
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    return [c for c in principal.calendars()]

def check_exist_calendars_by_cal_id(user: Row, cals_id: list[str, ...]) -> list[Calendar, ...] | dict:
    principal = take_principal(user)

    if type(principal) is dict:
        return principal

    cals = []

    for cal_id in cals_id:

        cal = principal.calendar(cal_id=cal_id)

        try:

            cal.objects()

        except caldav_errs.NotFoundError as exp:

            return {
                'type': 'error',
                'text': f'Calendar with {cal_id=} doesn\'t exist. Notification scheduler was deleted.',
            }

        else:
            cals.append(cal)

    return cals


def get_conferences_with_some_cals(cals: list[Calendar, ...], timezone) -> list[Conference, ...]:
    start = datetime.now(UTC).astimezone(ZoneInfo(timezone))
    end = start + timedelta(days=365 * 4)

    return caldav_searchers.find_conferences_in_some_cals(cals, (start, end))


def get_conferences_with_one_cal(cal: Calendar, timezone) -> list[Conference, ...]:
    start = datetime.now(UTC).astimezone(ZoneInfo(timezone))
    end = start + timedelta(days=365 * 4)

    return caldav_searchers.find_conferences_in_one_cal(cal, (start, end))
