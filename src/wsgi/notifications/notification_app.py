from wsgi.decorators.account_decorators import auth_required
from wsgi.notifications import notification_handlers

from flask import Blueprint, request, g

bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@bp.route('create_notification', methods=['POST'])
@auth_required
def create_notification():
    return notification_handlers.create_notifications(g.user, request)


@bp.route('continue_create_notification', methods=['POST'])
@auth_required
def continue_create_notification():
    return notification_handlers.continue_create_notifications(g.user, request)


@bp.route('update_notification', methods=['POST'])
@auth_required
def update_notification():
    return notification_handlers.update_notifications(g.user, request)


@bp.route('delete_notification', methods=['POST'])
@auth_required
def delete_notification():
    return notification_handlers.delete_notifications(request)
