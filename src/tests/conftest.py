import asyncio, pytest

from caldav import Principal
from dramatiq import Worker
from httpx import HTTPError

import settings
from app.bots.bot_commands import get_user_by_username, create_user
from app.calendars import caldav_api
from app.calendars.caldav_funcs import take_principal
from app.notifications.tasks import broker

# init testing environments
settings.Conf = settings.Testing
from settings import Conf
from app import create_app


async def init_scope():
    global test_user, mm_user_id, test_principal, test_calendar1, test_calendar2
    # create test user, if it doesn't exist
    test_user = await get_user_by_username(username=Conf.test_client_username)

    if isinstance(test_user, HTTPError):
        test_user = await create_user({
            'email': Conf.test_client_email,
            'username': Conf.test_client_username,
            'first_name': Conf.test_client_first_name,
            'last_name': Conf.test_client_last_name,
            'nickname': Conf.test_client_nickname,
            'password': Conf.test_client_password,
        })

    mm_user_id = test_user['id']

    test_principal = await take_principal(Conf.test_client_ya_login, Conf.test_client_ya_token)
    assert type(test_principal) is Principal

    test_calendar1 = await caldav_api.get_calendar_by_name(test_principal, Conf.test_client_calendar_name1)
    if type(test_calendar1) is dict:
        test_calendar1 = await caldav_api.create_calendar(test_principal, name=Conf.test_client_calendar_name1)

    test_calendar2 = await caldav_api.get_calendar_by_name(test_principal, Conf.test_client_calendar_name2)
    if type(test_calendar2) is dict:
        test_calendar2 = await caldav_api.create_calendar(test_principal, name=Conf.test_client_calendar_name2)


if Conf.TESTING:
    asyncio.get_event_loop().run_until_complete(init_scope())


@pytest.fixture  # (scope="session")
def app():
    app = create_app()

    yield app


@pytest.fixture  # (scope="session")
def client(app):
    return app.test_client()


@pytest.fixture  # (scope="session")
def runner(app):
    return app.test_cli_runner()


@pytest.fixture  # (scope="session")
def stub_broker():
    broker.flush_all()
    return broker


@pytest.fixture  # (scope="session")
def stub_worker():
    worker = Worker(broker, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()
