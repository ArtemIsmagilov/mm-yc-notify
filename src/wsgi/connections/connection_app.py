from wsgi.decorators.account_decorators import auth_required, required_account_does_not_exist
from wsgi.connections import connection_handlers

from flask import Blueprint, request, g

bp = Blueprint('connections', __name__, url_prefix='/connections')


@bp.route('really_delete', methods=['POST'])
@auth_required
def really_delete() -> dict:
    return connection_handlers.really_delete(request)


@bp.route('disconnect', methods=['POST'])
@auth_required
def disconnect() -> dict:
    return connection_handlers.delete_account(request, g.user)


@bp.route('really_update', methods=['POST'])
@auth_required
def really_update() -> dict:
    return connection_handlers.really_update(request)


@bp.route('update_form', methods=['POST'])
@auth_required
def update_form() -> dict:
    return connection_handlers.update_form()


@bp.route('update', methods=['POST'])
@auth_required
def update() -> dict:
    return connection_handlers.update_account(request, g.user)


@bp.route('connect', methods=['POST'])
@required_account_does_not_exist
def connect() -> dict:
    return connection_handlers.create_account(request)


@bp.route('profile', methods=['POST'])
@auth_required
def profile() -> dict:
    return connection_handlers.profile(g.user, request)
