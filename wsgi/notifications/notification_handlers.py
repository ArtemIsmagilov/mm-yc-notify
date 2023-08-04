from wsgi.converters import get_hours_minutes_with_UTC_from_form, get_dt_with_UTC_tz_from_iso
from wsgi.app_handlers import static_file
from wsgi.calendars import caldav_api
from wsgi.constants import EXPAND_DICT, TIMEs
from wsgi.notifications import jobs
from wsgi.schedulers.sd import scheduler, delete_jobs_by_user_id, check_exists_jobs_by_user_id

from datetime import timedelta

from flask import Request, render_template, url_for
from sqlalchemy.engine import Row
import logging


def delete_notifications(request: Request):
    context = request.json['context']
    acting_user = context['acting_user']
    user_id, mm_username = acting_user['id'], acting_user['username']

    if not check_exists_jobs_by_user_id(user_id):

        return {

            'type': 'ok',
            'text': '# @{}, you don\'t have scheduler notifications'.format(mm_username),

        }

    else:

        delete_jobs_by_user_id(user_id)

        return {

            'type': 'ok',
            'text': '# @{}, you successfully DELETE scheduler notifications'.format(mm_username),

        }


def update_notifications(user: Row, request: Request):
    delete_jobs_by_user_id(user.user_id)

    return create_notifications(user, request)


def create_notifications(user: Row, request: Request):
    context = request.json['context']
    acting_user = context['acting_user']
    user_id, mm_username = acting_user['id'], acting_user['username']

    if check_exists_jobs_by_user_id(user_id):
        return {
            'type': 'error',
            'text': '# @{}, you already have notify scheduler\n'.format(mm_username),
        }

    principal = caldav_api.take_principal(user)

    if type(principal) is dict:
        return principal

    cals = [{"label": c.name, "value": c.name} for c in principal.calendars() if caldav_api.exist_conferences_view(c)]

    if not cals:
        return {'type': 'error', 'text': 'You don\'t have a calendars with conferences'}

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
                    "name": "Calendar",
                    "type": "static_select",
                    "label": "cal",
                    "modal_label": 'Calendar',
                    "options": cals,
                    "is_required": True,
                    "description": 'Select yandex calendar',
                    "value": cals[0],
                    "hint": '[Calendar display name]'
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


def continue_create_notifications(user: Row, request: Request):
    context = request.json['context']
    acting_user = context['acting_user']
    user_id, mm_username = acting_user['id'], acting_user['username']

    job_id_daily = f'{user_id}(daily)'
    job_id_before_status = f'{user_id}(before-status)'

    values = request.json["values"]

    calendar_name = values['Calendar']['value']
    daily_clock = values['Time']['value']
    notification_before_10_min = values['Notification']
    status = values['Status']

    h, m = get_hours_minutes_with_UTC_from_form(daily_clock, user.timezone)

    user_id = context['acting_user']['id']

    # required job1 daily notification at current clock

    job1 = scheduler.add_job(

        func=jobs.daily_notification_job,
        trigger='cron',
        args=(user_id, calendar_name),
        id=job_id_daily,
        name=user.login,
        replace_existing=True,
        minute=m,
        hour=h,

    )

    # job2 if notification_before_10_min or status (is optional)
    if notification_before_10_min or status:

        representation = caldav_api.first_conference_notification(user, calendar_name)

        if representation.get('type') != 'ok':
            return representation

        first_conferences = representation.get('first_conferences')

        if not first_conferences:

            return {

                'type': representation.get('type'),
                'text': representation.get('text'),

            }

        else:

            first_conf = first_conferences[0]

            start_job = get_dt_with_UTC_tz_from_iso(first_conf.dtstart) - timedelta(minutes=10)

            job2 = scheduler.add_job(

                func=jobs.notify_next_conference_job,
                trigger='date',
                args=(user_id, calendar_name, first_conf.uid, notification_before_10_min, status),
                id=job_id_before_status,
                name=user.login,
                replace_existing=True,
                run_date=start_job,

            )

            return {
                'type': 'ok',
                'text': render_template(

                    'created_jobs.md',
                    mm_username=mm_username,
                    calendar_name=calendar_name,
                    timezone=user.timezone,
                    daily_clock=daily_clock,
                    notification_before_10_min=notification_before_10_min,
                    status=status,

                )
            }
