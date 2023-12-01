from ..connections import connection_handlers

from quart import Blueprint

bp = Blueprint('connections', __name__, url_prefix='/connections')


@bp.post('profile_account')
async def profile_account() -> dict:
    return await connection_handlers.profile()


@bp.post('connect_account')
async def connect_account() -> dict:
    return await connection_handlers.create_account()


@bp.post('really_update_account')
async def really_update_account() -> dict:
    return await connection_handlers.really_update_account()


@bp.post('update_account_form')
async def update_account_form() -> dict:
    return connection_handlers.update_account_form()


@bp.post('update_account')
async def update_account() -> dict:
    return await connection_handlers.update_account()


@bp.post('really_delete_account')
async def really_delete_account() -> dict:
    return await connection_handlers.really_delete_account()


@bp.post('disconnect_account')
async def disconnect_account() -> dict:
    return await connection_handlers.delete_account()
