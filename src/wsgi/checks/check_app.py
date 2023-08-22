from wsgi.checks import check_my_account, check_my_scheduler
from wsgi.decorators.account_decorators import auth_required


from flask import Blueprint, g, request

bp = Blueprint('checks', __name__, url_prefix='/checks')


@bp.route('check_account', methods=['POST'])
def check_account() -> dict:
    return check_my_account.check_user(g.user)


@bp.route('check_scheduler', methods=['POST'])
@auth_required
def check_scheduler() -> dict:
    return check_my_scheduler.check_scheduler(request)
