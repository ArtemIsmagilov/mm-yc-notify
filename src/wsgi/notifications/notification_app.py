from wsgi.decorators.account_decorators import auth_required
from wsgi.notifications import notification_handlers

from flask import Blueprint, request, g

bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@bp.route('create_notification', methods=['POST'])
@auth_required
def create_notification() -> dict:
    return notification_handlers.create_notification(g.user, request)


@bp.route('continue_create_notification', methods=['POST'])
@auth_required
def continue_create_notification() -> dict:
    return notification_handlers.continue_create_notification(g.user, request)


@bp.route('really_update_notification', methods=['POST'])
@auth_required
def really_update_notification() -> dict:
    return notification_handlers.really_update_notification(g.user, request)


@bp.route('update_notification', methods=['POST'])
@auth_required
def update_notification() -> dict:
    return notification_handlers.update_notification(g.user, request)


@bp.route('continue_update_notification', methods=['POST'])
@auth_required
def continue_update_notification() -> dict:
    return notification_handlers.continue_update_notification(g.user, request)


@bp.route('really_delete_notification', methods=['POST'])
@auth_required
def really_delete_notification() -> dict:
    return notification_handlers.really_delete_notification(g.user, request)


@bp.route('delete_notification', methods=['POST'])
@auth_required
def delete_notification() -> dict:
    return notification_handlers.delete_notification(g.user, request)
