from .constants import EXPAND_DICT, UTCs
from settings import Conf
from quart import url_for, render_template, request


def static_file(filename) -> str:
    return '%s/%s/%s' % (Conf.APP_URL_EXTERNAL, 'static', filename)


async def help_info() -> dict:
    data = await request.json
    mm_username = data['context']['acting_user']['username']
    text = await render_template('info.md', mm_username=mm_username)

    return {
        'type': 'ok',
        'text': text,
    }


def bindings() -> dict:
    return {
        'type': 'ok',
        'data': [
            {
                'location': '/command',
                'bindings': [
                    {
                        'description': 'yandex calendar',
                        'hint': '[commands]',
                        'label': 'yandex-calendar',
                        'icon': static_file('cal.png'),
                        'bindings': [
                            {
                                'description': 'connections',
                                'hint': '[connect|disconnect|update|profile]',
                                'label': 'connections',
                                'icon': static_file('cal.png'),
                                'bindings': [
                                    {
                                        "location": "connect",
                                        "label": "connect",
                                        "description": "Create integration to yandex calendar(CalDAV)",
                                        "form": {
                                            "title": "Create integrations with Yandex Calendar over CalDAV protocol",
                                            "header": "Connect",
                                            "icon": static_file('cal.png'),
                                            "fields": [
                                                {
                                                    "name": "login",
                                                    "label": "login",
                                                    "modal_label": 'Login',
                                                    "type": "text",
                                                    "subtype": "input",
                                                    "description": "Enter login",
                                                    'is_required': True,
                                                    'hint': '[login]'
                                                },
                                                {
                                                    "name": "token",
                                                    "label": "token",
                                                    "modal_label": 'Token',
                                                    "type": "text",
                                                    "subtype": "password",
                                                    "description": "Enter created yandex calendar app token",
                                                    'hint': '[token]',
                                                    'is_required': True,
                                                },
                                                {
                                                    "name": "timezone",
                                                    "type": "static_select",
                                                    "label": "utc",
                                                    "modal_label": 'TimeZone',
                                                    "options": UTCs,
                                                    "is_required": True,
                                                    "description": 'Select timezone',
                                                    "value": {'label': '(UTC+00:00) UTC', 'value': 'UTC'},
                                                    "hint": '[(UTC-12)|(UTC+12)]',
                                                },
                                            ],
                                            "submit": {
                                                "path": url_for('connections.connect_account'),
                                                'expand': EXPAND_DICT,
                                            }
                                        }
                                    },
                                    {
                                        "location": "profile",
                                        "label": "profile",
                                        "description": "Profile integration to yandex calendar(CalDAV)",
                                        "form": {
                                            "title": "Profile integrations with Yandex Calendar over CalDAV protocol",
                                            "header": "Connect",
                                            "icon": static_file("cal.png"),
                                            "submit": {
                                                "path": url_for("connections.profile_account"),
                                                "expand": EXPAND_DICT,
                                            },

                                        },
                                    },
                                    {
                                        "location": "update",
                                        "label": "update",
                                        "description": "update to yandex calendar(CalDAV)",
                                        "form": {
                                            "title": "Update to integrations with yandex calendar",
                                            "header": "Updating",
                                            "icon": static_file('cal.png'),
                                            "submit": {
                                                "path": url_for('connections.really_update_account'),
                                                'expand': EXPAND_DICT,
                                            }
                                        }
                                    },
                                    {
                                        "location": "disconnect",
                                        "label": "disconnect",
                                        "description": "disconnect to yandex calendar(CalDAV)",
                                        "form": {
                                            "title": "Disconnect to integrations with yandex calendar",
                                            "header": "Disconnecting",
                                            "icon": static_file('cal.png'),
                                            "submit": {
                                                "path": url_for('connections.really_delete_account'),
                                                'expand': EXPAND_DICT,
                                            }
                                        }
                                    },
                                ],
                            },
                            {
                                'description': 'calendars',
                                'hint': '[get_a_week|get_a_month|current|today|from_to]',
                                'label': 'calendars',
                                'icon': static_file('cal.png'),
                                'bindings': [
                                    {
                                        "location": "get_a_week",
                                        "label": "get_a_week",
                                        "description": "Show all calendars to yandex-calendar(CalDAV)",
                                        "form": {
                                            "title": "All conferences (CalDAV) a week in yandex-calendars",
                                            "header": "get_a_week",
                                            "icon": static_file('cal.png'),
                                            "submit": {
                                                "path": url_for('calendars.get_a_week'),
                                                'expand': EXPAND_DICT,
                                            }
                                        }
                                    },
                                    {
                                        "location": "get_a_month",
                                        "label": "get_a_month",
                                        "description": "Show all calendars to yandex-calendar(CalDAV)",
                                        "form": {
                                            "title": "All conferences (CalDAV) a month in yandex-calendars",
                                            "header": "get_a_month",
                                            "icon": static_file('cal.png'),
                                            "submit": {
                                                "path": url_for('calendars.get_a_month'),
                                                'expand': EXPAND_DICT,
                                            }
                                        }
                                    },
                                    {
                                        "location": "current",
                                        "label": "current",
                                        "description": "Get conference by date",
                                        "form": {
                                            "title": "Get conference by date",
                                            "header": "current",
                                            "icon": static_file('cal.png'),
                                            "fields": [
                                                {
                                                    "name": "date",
                                                    "label": "date",
                                                    "type": "text",
                                                    "subtype": "input",
                                                    "description": "format to date: DD.MM.YYYY",
                                                    'is_required': True,
                                                    'hint': 'Example: 01.01.2023'
                                                },
                                            ],
                                            "submit": {
                                                "path": url_for('calendars.current'),
                                                'expand': EXPAND_DICT,
                                            }
                                        }
                                    },
                                    {
                                        "location": "from_to",
                                        "label": "from_to",
                                        "description": "Get conference by date from start to end date",
                                        "form": {
                                            "title": "From start to end date",
                                            "header": "from_to",
                                            "icon": static_file('cal.png'),
                                            "fields": [
                                                {
                                                    "name": "from_date",
                                                    "label": "from_date",
                                                    "type": "text",
                                                    "subtype": "input",
                                                    "description": "format to date: DD.MM.YYYY",
                                                    'is_required': True,
                                                    'hint': 'Example: 01.01.2023'
                                                },
                                                {
                                                    "name": "to_date",
                                                    "label": "to_date",
                                                    "type": "text",
                                                    "subtype": "input",
                                                    "description": "format to date: DD.MM.YYYY",
                                                    'is_required': True,
                                                    'hint': 'Example: 01.02.2023'
                                                },
                                            ],
                                            "submit": {
                                                "path": url_for('calendars.from_to'),
                                                'expand': EXPAND_DICT,
                                            }
                                        }
                                    },
                                    {
                                        "location": "today",
                                        "label": "today",
                                        "description": "Get conference by today",
                                        "form": {
                                            "title": "Get conference by today",
                                            "header": "today",
                                            "icon": static_file('cal.png'),
                                            "submit": {
                                                "path": url_for('calendars.today'),
                                                'expand': EXPAND_DICT,
                                            }
                                        }
                                    },
                                ],
                            },
                            {
                                'description': 'notifications',
                                'hint': '[create|update|delete]',
                                'label': 'notifications',
                                'icon': static_file('cal.png'),
                                'bindings': [
                                    {
                                        "location": "create",
                                        "label": "create",
                                        "description": "create notification for integration with yandex calendar",
                                        "submit": {
                                            "path": url_for('notifications.create_notification'),
                                            'expand': EXPAND_DICT,
                                        }
                                    },
                                    {
                                        "location": "update",
                                        "label": "update",
                                        "description": "update notification for integration with yandex calendar",
                                        "submit": {
                                            "path": url_for('notifications.really_update_notification'),
                                            'expand': EXPAND_DICT,
                                        }
                                    },
                                    {
                                        "location": "delete",
                                        "label": "delete",
                                        "description": "delete notification for integration with yandex calendar",
                                        "submit": {
                                            "path": url_for('notifications.really_delete_notification'),
                                            'expand': EXPAND_DICT,
                                        }
                                    },
                                ],
                            },
                            {
                                'description': 'checks',
                                'hint': '[checking account and activation scheduler notifications]',
                                'label': 'checks',
                                'icon': static_file('cal.png'),
                                'bindings': [
                                    {
                                        "location": "check_account",
                                        "label": "check_account",
                                        "description": "check me integration with yandex calendar",
                                        "submit": {
                                            "path": url_for('checks.check_account'),
                                            'expand': EXPAND_DICT,
                                        }
                                    },
                                    {
                                        "location": "check_scheduler",
                                        "label": "check_scheduler",
                                        "description": "check my scheduler in integration with yandex calendar",
                                        "submit": {
                                            "path": url_for('checks.check_scheduler'),
                                            'expand': EXPAND_DICT,
                                        }
                                    },
                                ],
                            },
                            {
                                'description': 'info about app',
                                'hint': '[help information about all commands app]',
                                'label': 'info',
                                'icon': static_file('cal.png'),
                                'bindings': [
                                    {
                                        "location": "help_info",
                                        "label": "help_info",
                                        "description": "help info app",
                                        "submit": {
                                            "path": url_for('help_info'),
                                            'expand': EXPAND_DICT,
                                        }
                                    },
                                ],
                            },
                        ],
                    },
                ],
            }
        ]
    }


def manifest() -> dict:
    return {
        'app_id': 'yandex-calendar',
        'homepage_url': 'https://github.com/ArtemIsmagilov/mm-yc-notify',
        'version': 'v1.0.2',
        'display_name': 'Yandex Calendar',
        'description': 'Integration your yandex calendar with Mattermost server on protocol CalDAV',
        'icon': 'cal.png',
        'requested_permissions': ['act_as_bot', 'act_as_user', 'remote_webhooks'],
        'requested_locations': ['/command'],
        'bindings': {
            'path': '/bindings',
        },
        'remote_webhook_auth_type': 'secret',
        'app_type': 'http',
        'on_install': {
            'path': '/install',
            'expand': EXPAND_DICT,
        },
        'on_uninstall': {
            'path': '/uninstall',
            'expand': EXPAND_DICT,
        },
        'http': {
            'root_url': Conf.APP_URL_EXTERNAL,
        },
    }
