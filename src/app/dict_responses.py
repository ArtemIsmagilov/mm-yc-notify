def success_create_integration(mm_username: str):
    return {
        'type': 'ok',
        'text': '# @%s, you successfully CREATE integration with yandex calendar.' % mm_username
    }


def success_remove_integration(mm_username: str):
    text = ('# @%s, you successfully REMOVE integration with yandex calendar. '
            'Your scheduler notifications was deleted if is existed.' % mm_username)

    return {
        'type': 'ok',
        'text': text,
    }


def success_update_integration(mm_username: str):
    text = ('# @%s, you successfully UPDATE integration with yandex calendar. '
            'Your scheduler notifications was deleted if is existed.') % mm_username
    return {
        'type': 'ok',
        'text': text,
    }


def already_exists_integration(mm_username: str):
    return {
        'type': 'error',
        'text': '# %s, your integration with yandex-calendar already exists.' % mm_username
    }


def unauth_integration(mm_username: str):
    return {
        'type': 'error',
        'text': '# @%s, your haven\'t integration with yandex-calendar. First, to connect.' % mm_username
    }


def incorrect_principal():
    return {
        'type': 'error',
        'text': '# Incorrect username or token. Possible, you changed the username and password.'
    }


def dav_error():
    return {
        'type': 'error',
        'text': '# Unknown Error. Please, contact with your admin platform.'
    }


def is_enable_integration(mm_username: str):
    return {
        'type': 'ok',
        'text': '# @%s, your integration with Yandex Calendar is enable :).' % mm_username,
    }


def is_disable_integration(mm_username):
    return {
        'type': 'ok',
        'text': ('# @%s, your integration with Yandex Calendar is disable :(\n'
                 'You need complete connect to integration.') % mm_username,
    }


def is_enable_scheduler(mm_username: str):
    return {
        'type': 'ok',
        'text': '# @%s, your scheduler is enable :).' % mm_username,
    }


def is_disable_scheduler(mm_username: str):
    return {
        'type': 'ok',
        'text': '# @%s, you don\'t have scheduler notifications :(.' % mm_username,
    }


def is_exists_scheduler(mm_username: str):
    return {
        'type': 'error',
        'text': '# @%s, you already have notify scheduler.' % mm_username,
    }


def no_scheduler(mm_username: str):
    return {
        'type': 'error',
        'text': '# @%s, you don\'t have scheduler notifications' % mm_username
    }


def success_remove_scheduler(mm_username: str):
    return {
        'type': 'ok',
        'text': '# @%s, you successfully DELETE scheduler notifications' % mm_username,
    }


def wrong_format_dates_from_to(mm_username: str, dtstart: str, dtend: str):
    return {
        'type': 'error',
        'text': '# @%s, wrong format from date and to date: %s, %s.' % (mm_username, dtstart, dtend)
    }


def wrong_format_date_current(mm_username: str, dt: str):
    return {
        'type': 'error',
        'text': '# %s, wrong format date. -> %s.' % (mm_username, dt)
    }


def calendar_dosnt_exists():
    return {
        'type': 'error',
        'text': '# Calendar doesn\'t exist.',
    }


def calendar_not_found():
    return {
        'type': 'error',
        'text': '# Calendar not found in yandex calendar server.'
    }


def no_calendars_on_server():
    return {
        'type': 'error',
        'text': '# You haven\'t calendars on CalDAV server.'
    }


def success_ok(mm_username: str):
    return {
        'type': 'ok',
        'text': '# Ok, @%s.' % mm_username
    }


def daily_no_conferences():
    return {
        'type': 'ok',
        'text': '# Today you don\'t have conferences',
    }


def invalid_clock_string():
    return {
        'type': 'error',
        'text': '# Incorrect format `Time` field.',
    }


def timeout_task():
    return {
        'type': 'error',
        "text": '# Timeout! Long operation.'
    }
