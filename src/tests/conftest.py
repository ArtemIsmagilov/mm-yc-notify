import pytest, caldav
from httpx import HTTPError
from icalendar import Event

from wsgi import create_app, settings
from wsgi.bots.mm_bot import get_user_by_username, create_user
from wsgi.calendars.caldav_api import check_exist_calendars_by_cal_id, take_principal
from wsgi.database import db

# init testing environments
settings.envs = settings.Testing()

# create test user, if it doesn't exist
test_user = get_user_by_username(username=settings.envs.test_client_username)

if isinstance(test_user, HTTPError):
    test_user = create_user({
        'email': settings.envs.test_client_email,
        'username': settings.envs.test_client_username,
        'first_name': settings.envs.test_client_first_name,
        'last_name': settings.envs.test_client_last_name,
        'nickname': settings.envs.test_client_nickname,
        'password': settings.envs.test_client_password,
    })

mm_user_id, mm_username = test_user['id'], test_user['username']


@pytest.fixture
def app():
    app = create_app()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
