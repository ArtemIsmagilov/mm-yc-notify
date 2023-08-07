from wsgi.decorators.account_decorators import auth_required
from wsgi.calendars import caldav_api

from flask import Blueprint, g, request

bp = Blueprint('calendars', __name__, url_prefix='/calendars')


@bp.route('get_a_week', methods=['POST'])
@auth_required
def get_a_week():
    return caldav_api.get_a_week(g.user)


@bp.route('get_a_month', methods=['POST'])
@auth_required
def get_a_month():
    return caldav_api.get_a_month(g.user)


@bp.route('current', methods=['POST'])
@auth_required
def current():
    return caldav_api.current(g.user, request)


@bp.route('today', methods=['POST'])
@auth_required
def today():
    return caldav_api.today(g.user)


@bp.route('from_to', methods=['POST'])
@auth_required
def from_to():
    return caldav_api.from_to(g.user, request)
