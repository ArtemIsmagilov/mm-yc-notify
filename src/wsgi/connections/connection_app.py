from wsgi.app_handlers import static_file
from wsgi.constants import EXPAND_DICT
from wsgi.decorators.account_decorators import auth_required, required_account_does_not_exist
from wsgi.connections import connection_handlers

from flask import Blueprint, request, url_for

bp = Blueprint('connections', __name__, url_prefix='/connections')


@bp.route('are_you_sure', methods=['POST'])
@auth_required
def are_you_sure():
    mm_username = request.json['context']['acting_user']['username']

    return {
        "type": "form",
        "form": {
            "title": "Delete connections?",
            "header": f'**{mm_username}**, are you sure, what need delete integration with yandex-calendar?',
            "icon": static_file('cal.png'),
            "submit": {
                "path": url_for('connections.disconnect'),
                "expand": EXPAND_DICT,
            },

        }
    }


@bp.route('connect', methods=['POST'])
@required_account_does_not_exist
def connect():
    return connection_handlers.create_account(request)


@bp.route('disconnect', methods=['POST'])
@auth_required
def disconnect():
    return connection_handlers.delete_account(request)


@bp.route('update', methods=['POST'])
@auth_required
def update():
    return connection_handlers.update_account(request)
