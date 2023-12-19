from ..calendars import caldav_api

from quart import Blueprint

bp = Blueprint('calendars', __name__, url_prefix='/calendars')


@bp.post('get_a_week')
async def get_a_week():
    return await caldav_api.get_a_week()


@bp.post('get_a_month')
async def get_a_month() -> dict:
    return await caldav_api.get_a_month()


@bp.post('current')
async def current() -> dict:
    return await caldav_api.current()


@bp.post('today')
async def today() -> dict:
    return await caldav_api.today()


# @bp.post('from_to')
# async def from_to() -> dict:
#     return await caldav_api.from_to()
