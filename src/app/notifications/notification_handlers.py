from .. import dict_responses
from ..calendars.caldav_api import get_calendar_by_cal_id
from ..notifications import tasks
from ..app_handlers import static_file
from ..calendars import caldav_api
from ..constants import EXPAND_DICT, TIMEs
from ..converters import get_h_m_utc, client_id_calendar, get_delay_daily
from ..decorators.account_decorators import dependency_principal, auth_required
from ..sql_app.crud import YandexCalendar, User

import asyncio
from typing import Generator
from quart import render_template, url_for, request
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncConnection
import caldav.lib.error as caldav_errs
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

    first_cal = await YandexCalendar.get_first_cal(conn, mm_user_id)

    if first_cal:
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

    first_cal = await YandexCalendar.get_first_cal(conn, mm_user_id)

    if first_cal:
        return dict_responses.is_exists_scheduler(mm_username)

    h, m = get_h_m_utc(daily_clock, user.timezone)

    result_cals_cal_id = await asyncio.gather(
        *(get_calendar_by_cal_id(principal, cal_id=c['value']) for c in cals_form)
    )

    try:
        result_sync_cals = await asyncio.gather(
            *(asyncio.to_thread(result_cal.objects_by_sync_token, load_objects=True)
              for result_cal in result_cals_cal_id)
            , return_exceptions=True
        )
    except caldav_errs.NotFoundError as exp:

        return dict_responses.calendar_not_found()

    sync_cals_in_db = [
        {'mm_user_id': user.mm_user_id, 'cal_id': sync_cal.calendar.id, 'sync_token': sync_cal.sync_token}
        for sync_cal in result_sync_cals
    ]

    async with asyncio.TaskGroup() as tg:

        tg.create_task(User.update_user(conn, user.mm_user_id, e_c=e_c, ch_stat=ch_stat))

        tg.create_task(YandexCalendar.add_many_cals(conn, sync_cals_in_db))

    async with asyncio.TaskGroup() as tg:

        for sync_cal in result_sync_cals:
            tg.create_task(tasks.load_updated_added_deleted_events(conn, user, sync_cal, notify=False))

    # required job1 daily notification at current clock

    delay = get_delay_daily(h, m)
    tasks.task1.send_with_options(args=(mm_user_id, h, m), delay=delay)

    # job2 if e_c or ch_stat (is optional)
    # in check event

    # job3 if CHECK_EVENTS
    # in check event

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

    first_cal = await YandexCalendar.get_first_cal(conn, mm_user_id)

    if first_cal:
        return dict_responses.is_exists_scheduler(mm_username)

    h, m = get_h_m_utc(daily_clock, user.timezone)

    result_cals_cal_id = await asyncio.gather(
        *(get_calendar_by_cal_id(principal, cal_id=c['value']) for c in cals_form)
    )

    try:
        result_sync_cals = await asyncio.gather(
            *(asyncio.to_thread(result_cal.objects_by_sync_token, load_objects=True)
              for result_cal in result_cals_cal_id)
            , return_exceptions=True
        )
    except caldav_errs.NotFoundError as exp:

        return dict_responses.calendar_not_found()

    sync_cals_in_db = [
        {'mm_user_id': user.mm_user_id, 'cal_id': sync_cal.calendar.id, 'sync_token': sync_cal.sync_token}
        for sync_cal in result_sync_cals
    ]

    async with asyncio.TaskGroup() as tg:

        tg.create_task(User.update_user(conn, user.mm_user_id, e_c=e_c, ch_stat=ch_stat))

        tg.create_task(YandexCalendar.add_many_cals(conn, sync_cals_in_db))

    async with asyncio.TaskGroup() as tg:

        for sync_cal in result_sync_cals:
            tg.create_task(tasks.load_updated_added_deleted_events(conn, user, sync_cal, notify=False))

    # required job1 daily notification at current clock

    delay = get_delay_daily(h, m)
    tasks.task1.send_with_options(args=(mm_user_id, h, m), delay=delay)

    # job2 if e_c or ch_stat (is optional)
    # in check event

    # job3 if CHECK_EVENTS
    # in check event

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

        await YandexCalendar.remove_cals(conn, mm_user_id)

        return dict_responses.success_remove_scheduler(mm_username)


def _form_calendars(calendars: list[Calendar]) -> Generator[dict, None, None]:
    for c in calendars:
        yield {'label': client_id_calendar(c), 'value': c.id}
