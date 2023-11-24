from . import notification_backgrounds
from .. import dict_responses
from ..app_handlers import static_file
from ..calendars import caldav_api
from ..constants import EXPAND_DICT, TIMEs
from ..converters import client_id_calendar
from ..decorators.account_decorators import dependency_principal, auth_required
from ..sql_app.crud import YandexCalendar

import asyncio
from typing import Generator
from quart import render_template, url_for, request
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncConnection
from caldav import Calendar, Principal


@auth_required
@dependency_principal
async def create_notification(
        conn: AsyncConnection,
        user: Row,
        principal: Principal,
) -> dict:
    data = await request.json
    context = data['context']
    acting_user = context['acting_user']
    mm_user_id, mm_username = acting_user['id'], acting_user['username']

    if await YandexCalendar.get_first_cal(conn, mm_user_id):
        return dict_responses.is_exists_scheduler(mm_username)

    exists_cals = await caldav_api.get_all_calendars(principal=principal)

    if type(exists_cals) is dict:
        return exists_cals

    cals = list(_form_calendars(exists_cals))

    return {
        "type": "form",
        "form": {
            "title": "Create notification",
            "icon": static_file("cal.png"),
            "submit": {
                "path": url_for("notifications.continue_create_notification"),
                'expand': EXPAND_DICT,
            },
            "fields": [
                {
                    "name": "Calendars",
                    "type": "static_select",
                    'multiselect': True,
                    "label": "cal",
                    "modal_label": 'Calendars',
                    "options": cals,
                    "is_required": True,
                    "description": 'Select yandex calendar(s)',
                    "hint": '[Calendars display name]'
                },
                {
                    "name": "Time",
                    "type": "static_select",
                    "label": "time",
                    "modal_label": 'Time',
                    "options": TIMEs,
                    "is_required": True,
                    "description": 'Select time for daily reminder',
                    "value": {'label': '07:00', 'value': '07:00'},
                    "hint": '[00:00-23.45]'
                },
                {
                    "name": "Notification",
                    "type": "bool",
                    "label": "Notification",
                    "modal_label": 'Notification',
                    "description": 'Notification and get info in 10 minutes before the start of the conference',
                    "value": True,
                    "hint": '[True|False]'
                },
                {
                    "name": "Status",
                    "type": "bool",
                    "label": "Status",
                    "modal_label": 'Status',
                    "description": 'Automatically change status on \'In a meeting\' when you on conference',
                    "value": True,
                    "hint": '[True|False]'
                },
            ]
        }
    }


@auth_required
@dependency_principal
async def continue_create_notification(
        conn: AsyncConnection,
        user: Row,
        principal: Principal,
) -> dict:
    data = await request.json
    context = data['context']
    acting_user = context['acting_user']
    mm_user_id, mm_username = acting_user['id'], acting_user['username']

    values = data["values"]

    cals_form = values['Calendars']

    daily_clock = values['Time']['value']

    e_c = values['Notification']
    ch_stat = values['Status']

    if await YandexCalendar.get_first_cal(conn, mm_user_id):
        return dict_responses.is_exists_scheduler(mm_username)

    asyncio.create_task(
        notification_backgrounds.bg_continue_create_notification(user, principal, cals_form, daily_clock, e_c, ch_stat)
    )

    return {
        'type': 'ok',
        'text': await render_template(
            'created_jobs.md',
            mm_username=mm_username,
            calendars_names=cals_form,
            timezone=user.timezone,
            daily_clock=daily_clock,
            e_c=e_c,
            ch_stat=ch_stat,
        )
    }


async def really_update_notification():
    data = await request.json
    mm_username = data['context']['acting_user']['username']

    return {
        "type": "form",
        "form": {
            "title": "Update scheduler?",
            "header": f'**{mm_username}**, are you sure, what need update your scheduler?',
            "icon": static_file('cal.png'),
            "submit": {
                "path": url_for('notifications.update_notification'),
                "expand": EXPAND_DICT,
            },
        }
    }


@auth_required
@dependency_principal
async def update_notification(
        conn: AsyncConnection,
        user: Row,
        principal: Principal,
) -> dict:
    data = await request.json
    context = data['context']
    acting_user = context['acting_user']
    mm_user_id, mm_username = acting_user['id'], acting_user['username']

    if not await YandexCalendar.get_first_cal(conn, mm_user_id):
        return dict_responses.no_scheduler(mm_username)

    exists_cals = await caldav_api.get_all_calendars(principal=principal)

    if type(exists_cals) is dict:
        return exists_cals

    cals = list(_form_calendars(exists_cals))

    return {
        "type": "form",
        "form": {
            "title": "Update notification",
            "icon": static_file("cal.png"),
            "submit": {
                "path": url_for("notifications.continue_update_notification"),
                'expand': EXPAND_DICT,
            },
            "fields": [
                {
                    "name": "Calendars",
                    "type": "static_select",
                    'multiselect': True,
                    "label": "cal",
                    "modal_label": 'Calendars',
                    "options": cals,
                    "is_required": True,
                    "description": 'Select yandex calendar(s)',
                    "hint": '[Calendars display name]'
                },
                {
                    "name": "Time",
                    "type": "static_select",
                    "label": "time",
                    "modal_label": 'Time',
                    "options": TIMEs,
                    "is_required": True,
                    "description": 'Select time for daily reminder',
                    "value": {'label': '07:00', 'value': '07:00'},
                    "hint": '[00:00-23.45]'
                },
                {
                    "name": "Notification",
                    "type": "bool",
                    "label": "Notification",
                    "modal_label": 'Notification',
                    "description": 'Notification and get info in 10 minutes before the start of the conference',
                    "value": True,
                    "hint": '[True|False]'
                },
                {
                    "name": "Status",
                    "type": "bool",
                    "label": "Status",
                    "modal_label": 'Status',
                    "description": 'Automatically change status on \'In a meeting\' when you on conference',
                    "value": True,
                    "hint": '[True|False]'
                },
            ]
        }
    }


@auth_required
@dependency_principal
async def continue_update_notification(
        conn: AsyncConnection,
        user: Row,
        principal: Principal,
):
    await YandexCalendar.remove_cals(conn, user.mm_user_id)
    # copy ->  continue_create_notification
    data = await request.json
    context = data['context']
    acting_user = context['acting_user']
    mm_user_id, mm_username = acting_user['id'], acting_user['username']

    values = data["values"]

    cals_form = values['Calendars']

    daily_clock = values['Time']['value']

    e_c = values['Notification']
    ch_stat = values['Status']

    if await YandexCalendar.get_first_cal(conn, mm_user_id):
        return dict_responses.is_exists_scheduler(mm_username)

    asyncio.create_task(
        notification_backgrounds.bg_continue_create_notification(user, principal, cals_form, daily_clock, e_c, ch_stat)
    )

    return {
        'type': 'ok',
        'text': await render_template(
            'created_jobs.md',
            mm_username=mm_username,
            calendars_names=cals_form,
            timezone=user.timezone,
            daily_clock=daily_clock,
            e_c=e_c,
            ch_stat=ch_stat,
        )
    }
    # copy ->  continue_create_notification


async def really_delete_notification():
    data = await request.json
    mm_username = data['context']['acting_user']['username']

    return {
        "type": "form",
        "form": {
            "title": "Delete scheduler?",
            "header": f'**{mm_username}**, are you sure, what need delete scheduler?',
            "icon": static_file('cal.png'),
            "submit": {
                "path": url_for('notifications.delete_notification'),
                "expand": EXPAND_DICT,
            },
        }
    }


@auth_required
async def delete_notification(
        conn: AsyncConnection,
        user: Row,
) -> dict:
    data = await request.json
    context = data['context']
    acting_user = context['acting_user']
    mm_user_id, mm_username = acting_user['id'], acting_user['username']

    if not await YandexCalendar.get_first_cal(conn, mm_user_id):

        return dict_responses.no_scheduler(mm_username)

    else:
        asyncio.create_task(notification_backgrounds.bg_remove_notification(mm_user_id))

        return dict_responses.success_remove_scheduler(mm_username)


def _form_calendars(calendars: list[Calendar]) -> Generator[dict, None, None]:
    for c in calendars:
        yield {'label': client_id_calendar(c), 'value': c.id}
