import functools
from flask import g


def auth_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return {
                'type': 'error',
                'text': 'Your haven\'t integration with yandex-calendar. First, to connect'
            }

        return view(**kwargs)

    return wrapped_view


def required_account_does_not_exist(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            return {
                'type': 'error',
                'text': 'Your integration with yandex-calendar already exists.'
            }

        return view(**kwargs)

    return wrapped_view
