from wsgi.app_handlers import static_file
from wsgi.constants import EXPAND_DICT
from wsgi.decorators.account_decorators import auth_required, required_account_does_not_exist
from wsgi.connections import connection_handlers

from flask import Blueprint, request, url_for, g

bp = Blueprint('connections', __name__, url_prefix='/connections')


@bp.route('are_you_sure', methods=['POST'])
@auth_required
def are_you_sure() -> dict:
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
def connect() -> dict:
    return connection_handlers.create_account(request)


@bp.route('disconnect', methods=['POST'])
@auth_required
def disconnect() -> dict:
    return connection_handlers.delete_account(request, g.user)


@bp.route('update', methods=['POST'])
@auth_required
def update() -> dict:
    return connection_handlers.update_account(request, g.user)


@bp.route('profile', methods=['POST'])
@required_account_does_not_exist
def profile() -> dict:
    return connection_handlers.profile(request)
