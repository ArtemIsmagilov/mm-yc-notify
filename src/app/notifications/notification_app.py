from ..notifications import notification_handlers

from quart import Blueprint

bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@bp.route('create_notification', methods=['POST'])
async def create_notification() -> dict:
    return await notification_handlers.create_notification()


@bp.route('continue_create_notification', methods=['POST'])
async def continue_create_notification() -> dict:
    return await notification_handlers.continue_create_notification()


@bp.route('really_update_notification', methods=['POST'])
async def really_update_notification() -> dict:
    return await notification_handlers.really_update_notification()


@bp.route('update_notification', methods=['POST'])
async def update_notification() -> dict:
    return await notification_handlers.update_notification()


@bp.route('continue_update_notification', methods=['POST'])
async def continue_update_notification() -> dict:
    return await notification_handlers.continue_update_notification()


@bp.route('really_delete_notification', methods=['POST'])
async def really_delete_notification() -> dict:
    return await notification_handlers.really_delete_notification()


@bp.route('delete_notification', methods=['POST'])
async def delete_notification() -> dict:
    return await notification_handlers.delete_notification()
