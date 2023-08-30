from wsgi.decorators.account_decorators import auth_required, required_account_does_not_exist
from wsgi.connections import connection_handlers

from flask import Blueprint, request, g

bp = Blueprint('connections', __name__, url_prefix='/connections')


@bp.route('profile_account', methods=['POST'])
def profile_account() -> dict:
    return connection_handlers.profile(g.user, request)


@bp.route('connect_account', methods=['POST'])
@required_account_does_not_exist
def connect_account() -> dict:
    return connection_handlers.create_account(request)


@bp.route('really_update_account', methods=['POST'])
@auth_required
def really_update_account() -> dict:
    return connection_handlers.really_update_account(request)


@bp.route('update_account_form', methods=['POST'])
@auth_required
def update_account_form() -> dict:
    return connection_handlers.update_account_form()


@bp.route('update_account', methods=['POST'])
@auth_required
def update_account() -> dict:
    return connection_handlers.update_account(request, g.user)


@bp.route('really_delete_account', methods=['POST'])
@auth_required
def really_delete_account() -> dict:
    return connection_handlers.really_delete_account(request)


@bp.route('disconnect_account', methods=['POST'])
@auth_required
def disconnect_account() -> dict:
    return connection_handlers.delete_account(request)
