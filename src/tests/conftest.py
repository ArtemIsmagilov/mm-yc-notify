import asyncio, pytest, uvloop
from caldav import Principal
from httpx import HTTPError
from icalendar import Event
from icalendar.prop import vDDDTypes, vCategory, vCalAddress
from datetime import datetime, UTC, timedelta

from app.bots.bot_commands import get_user_by_username, create_user, bot
from app.calendars.caldav_funcs import take_principal
from app.async_wraps.async_wrap_caldav import caldav_calendar_by_name, caldav_create_calendar
import settings
from app.calendars.conference import Conference

# init testing environments
settings.Conf = settings.Testing
from settings import Conf
from app import create_app


async def init_scope():
    global test_user, mm_user_id, channel_id, test_principal, test_calendar1, test_calendar2, test_context, test_conference


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
    response = await bot.channels.create_direct_channel([mm_user_id, bot.client.userid])
    channel_id = response['id']
    test_context = {'context': {'acting_user': {'id': mm_user_id, 'username': Conf.test_client_username},
                                'channel': {'id': channel_id},
                                }
                    }

    test_principal = await take_principal(Conf.test_client_ya_login, Conf.test_client_ya_token)
    assert type(test_principal) is Principal

    test_calendar1 = await caldav_calendar_by_name(test_principal, Conf.test_client_calendar_name1)
    if type(test_calendar1) is dict:
        test_calendar1 = await caldav_create_calendar(test_principal, name=Conf.test_client_calendar_name1)

    test_calendar2 = await caldav_calendar_by_name(test_principal, Conf.test_client_calendar_name2)
    if type(test_calendar2) is dict:
        test_calendar2 = await caldav_create_calendar(test_principal, name=Conf.test_client_calendar_name2)

    test_event = Event()
    test_event['UID'] = 'test_uid'
    test_event['DTSTART'] = vDDDTypes(datetime.now(UTC))
    test_event['DTEND'] = vDDDTypes(datetime.now(UTC) + timedelta(days=1))
    test_event['SUMMARY'] = 'test_summary'
    test_event['CREATED'] = test_event['DTSTART']
    test_event['LAST-MODIFIED'] = test_event['DTSTART']
    test_event['DESCRIPTION'] = 'test_description'
    test_event['URL'] = 'test_url'
    test_event['CATEGORIES'] = vCategory('test_category')
    test_event['X-TELEMOST-CONFERENCE'] = 'test_telemost_conference'
    test_event['ORGANIZER'] = vCalAddress('mailto:test_mail')
    test_event['ATTENDEE'] = [test_event['ORGANIZER'], vCalAddress('mailto:test_mail2')]
    test_event['LOCATION'] = 'test_location'
    test_event['RECURRENCE-ID'] = test_event['DTSTART']

    test_conference = Conference(test_event, Conf.test_client_ya_timezone)

if Conf.TESTING:
    asyncio.get_event_loop().run_until_complete(init_scope())


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


@pytest.fixture(scope="session")
def event_loop_policy():
    return uvloop.EventLoopPolicy()
