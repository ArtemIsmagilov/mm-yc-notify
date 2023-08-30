from wsgi.app_handlers import static_file
from wsgi.calendars import caldav_api
from wsgi.constants import EXPAND_DICT, TIMEs
from wsgi.converters import get_h_m
from wsgi.notifications import jobs
from wsgi.schedulers import sd
from wsgi.database import db
from wsgi.settings import CHECK_EVENTS

from flask import Request, render_template, url_for
from sqlalchemy.engine import Row
import caldav.lib.error as caldav_errs
from apscheduler.triggers.cron import CronTrigger


def create_notification(user: Row, request: Request) -> dict:
    context = request.json['context']
    acting_user = context['acting_user']
    mm_user_id, mm_username = acting_user['id'], acting_user['username']

    if db.YandexCalendar.get_cals(user_id=user.id):
        return {
            'type': 'error',
            'text': '# @{}, you already have notify scheduler\n'.format(mm_username),
        }

    exists_cals = caldav_api.get_all_calendars(user)

    if type(exists_cals) is dict:
        return exists_cals

    cals = [{"label": f'{c.get_display_name()}({c.id})', "value": c.id} for c in exists_cals]

    if not cals:
        return {
            'type': 'error',
            'text': 'You don\'t have a calendars with conferences'
        }

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


def continue_create_notification(user: Row, request: Request) -> dict:
    context = request.json['context']
    acting_user = context['acting_user']
    mm_user_id, mm_username = acting_user['id'], acting_user['username']

    values = request.json["values"]

    cals_form = values['Calendars']

    daily_clock = values['Time']['value']

    e_c = values['Notification']
    ch_stat = values['Status']

    calendars_names = (v['label'] for v in cals_form)

    h, m = get_h_m(daily_clock, user.timezone)

    principal = caldav_api.take_principal(user)

    if type(principal) is dict:
        return principal

    sync_cals = []

    for d in cals_form:
        cal_id = d['value']

        cal = principal.calendar(cal_id=cal_id)

        try:

            sync_cal = cal.objects(load_objects=True)

        except caldav_errs.NotFoundError as exp:

            db.YandexCalendar.remove_cal(cal_id=cal_id)

            return {
                'type': 'error',
                'text': f'Calendar with {cal_id=} not found in yandex calendar server',
            }

        else:

            db.YandexCalendar.add_one_cal(user_id=user.id, cal_id=cal_id, sync_token=sync_cal.sync_token)
            sync_cals.append(sync_cal)

    db.User.update_user(user.mm_user_id, login=user.login, token=user.token, timezone=user.timezone, e_c=e_c,
                        ch_stat=ch_stat)

    # required job1 daily notification at current clock
    job1 = sd.scheduler.add_job(
        func=jobs.daily_notification_job,
        trigger='cron',
        args=(mm_user_id,),
        id=f'{mm_user_id}(daily)',
        name=user.login,
        replace_existing=True,
        minute=m,
        hour=h,
    )

    # job2 if e_c or ch_stat (is optional)
    [jobs.load_updated_added_deleted_events(user, sync_cal, notify=False) for sync_cal in sync_cals]

    # job3 if CHECK_EVENTS does exist in env
    if CHECK_EVENTS:
        job3 = sd.scheduler.add_job(
            func=jobs.check_events_job,
            trigger=CronTrigger.from_crontab(CHECK_EVENTS),
            args=(mm_user_id,),
            id=f'{mm_user_id}(check-events)',
            name=user.login,
            replace_existing=True,
        )

    return {
        'type': 'ok',
        'text': render_template(
            'created_jobs.md',
            mm_username=mm_username,
            calendars_names=calendars_names,
            timezone=user.timezone,
            daily_clock=daily_clock,
            e_c=e_c,
            ch_stat=ch_stat,
        )
    }


def really_update_notification(user: Row, request: Request):
    mm_username = request.json['context']['acting_user']['username']

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


def update_notification(user: Row, request: Request) -> dict:
    context = request.json['context']
    acting_user = context['acting_user']
    mm_user_id, mm_username = acting_user['id'], acting_user['username']

    if not db.YandexCalendar.get_cals(user_id=user.id):
        return {
            'type': 'error',
            'text': '# @{}, you have not notify scheduler\n'.format(mm_username),
        }

    exists_cals = caldav_api.get_all_calendars(user)

    if type(exists_cals) is dict:
        return exists_cals

    cals = [{"label": f'{c.get_display_name()}({c.id})', "value": c.id} for c in exists_cals]

    if not cals:
        return {
            'type': 'error',
            'text': 'You don\'t have a calendars with conferences'
        }

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


def continue_update_notification(user: Row, request: Request):
    mm_user_id = request.json['context']['acting_user']['id']

    sd.delete_jobs_by_mm_user_id(mm_user_id)
    db.YandexCalendar.remove_cals(user_id=user.id)

    return continue_create_notification(user, request)


def really_delete_notification(user: Row, request: Request):
    mm_username = request.json['context']['acting_user']['username']

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


def delete_notification(user: Row, request: Request) -> dict:
    context = request.json['context']
    acting_user = context['acting_user']
    mm_user_id, mm_username = acting_user['id'], acting_user['username']

    if not db.YandexCalendar.get_cals(user_id=user.id):

        return {
            'type': 'ok',
            'text': '# @{}, you don\'t have scheduler notifications'.format(mm_username),
        }

    else:

        sd.delete_jobs_by_mm_user_id(mm_user_id)
        db.YandexCalendar.remove_cals(user_id=user.id)

        return {
            'type': 'ok',
            'text': '# @{}, you successfully DELETE scheduler notifications'.format(mm_username),
        }
