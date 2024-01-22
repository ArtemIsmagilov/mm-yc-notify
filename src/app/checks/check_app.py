from quart import Blueprint

from ..checks import (
    check_my_account,
    check_my_scheduler
)

bp = Blueprint('checks', __name__, url_prefix='/checks')


@bp.post('check_account')
async def check_account() -> dict:
    return await check_my_account.check_user()


@bp.post('check_scheduler')
async def check_scheduler() -> dict:
    return await check_my_scheduler.check_scheduler()
