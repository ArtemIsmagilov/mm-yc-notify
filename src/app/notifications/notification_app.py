from quart import Blueprint

from ..notifications import notification_handlers

bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@bp.post('create_notification')
async def create_notification() -> dict:
    return await notification_handlers.create_notification()


@bp.post('continue_create_notification')
async def continue_create_notification() -> dict:
    return await notification_handlers.continue_create_notification()


@bp.post('really_update_notification')
async def really_update_notification() -> dict:
    return await notification_handlers.really_update_notification()


@bp.post('update_notification')
async def update_notification() -> dict:
    return await notification_handlers.update_notification()


@bp.post('continue_update_notification')
async def continue_update_notification() -> dict:
    return await notification_handlers.continue_update_notification()


@bp.post('really_delete_notification')
async def really_delete_notification() -> dict:
    return await notification_handlers.really_delete_notification()


@bp.post('delete_notification')
async def delete_notification() -> dict:
    return await notification_handlers.delete_notification()
