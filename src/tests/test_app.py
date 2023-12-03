# before testing
# 0. add all needed values in .env file
# 1. docker compose down/up rabbitmq
# 2. docker compose down/up postgres
# 3. quart init-db -c
# 4. python -m app.notifications.task0_scheduler
# 5. dramatiq app.notifications.tasks

import asyncio, pytest
from copy import deepcopy

from app.async_wraps.async_wrap_caldav import caldav_create_calendar, caldav_calendar_by_name
from app.converters import get_h_m_utc
from app import dict_responses
from app.notifications import tasks
from app.sql_app.crud import User, YandexCalendar
from app.sql_app.database import get_conn

from .additional_funcs import decrease_user, increase_user, increase_calendar, modify_user
from .conftest import Conf, mm_user_id, channel_id, test_principal, test_calendar1, test_calendar2, test_context


@pytest.mark.asyncio(scope="module")
class TestApp:

    async def test_help_info(self, client, post_fix="/help_info"):
        data = test_context
        response = await client.post(post_fix, json=data)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_ping(self, client, post_fix="/ping"):
        response = await client.post(post_fix)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_install(self, client, post_fix="/install"):
        response = await client.post(post_fix)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_uninstall(self, client, post_fix="/uninstall"):
        response = await client.post(post_fix)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_bindings(self, client, post_fix="/bindings"):
        response = await client.post(post_fix)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_manifest(self, client, post_fix="/manifest.json"):
        response = await client.get(post_fix)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['app_id'] == 'yandex-calendar'


@pytest.mark.asyncio(scope="module")
class TestConnections:
    endpoint = "/connections/"

    @pytest.mark.parametrize('login,token,timezone', (
            ('', '', ''),
            ("fake_login", 'fake_token', 'UTC'),
            ("invalid_data", 'invalid_data', 'UTC'),
    ))
    async def test_incorrect_principal_connect_account(self, client, login, token, timezone,
                                                       post_fix="connect_account"):
        data = deepcopy(test_context)
        data.update({'values': {'login': login, 'token': token, 'timezone': {'value': timezone}}})

        response = await client.post(self.endpoint + post_fix, json=data)
        json_resp = await response.json

        assert response.status_code == 200
        assert json_resp == dict_responses.incorrect_principal()

    async def test_exist_account_connect_account(self, client, post_fix="connect_account"):
        data = deepcopy(test_context)
        data.update({'values': {
            'login': Conf.test_client_ya_login,
            'token': Conf.test_client_ya_token,
            'timezone': {'value': Conf.test_client_ya_timezone}
        }})

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.already_exists_integration(Conf.test_client_username)

    async def test_success_connect_account(self, client, post_fix="connect_account"):
        data = deepcopy(test_context)
        data.update({'values': {
            'login': Conf.test_client_ya_login,
            'token': Conf.test_client_ya_token,
            'timezone': {'value': Conf.test_client_ya_timezone}
        }})

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.success_create_integration(Conf.test_client_username)

    async def test_anonymous_profile_account(self, client, post_fix="profile_account"):
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.success_ok(Conf.test_client_username)

    @pytest.mark.parametrize('login,token,timezone', (
            ('', '', ''),
            ("fake_login", 'fake_token', 'UTC'),
            ("invalid_data", 'invalid_data', 'UTC'),
    ))
    async def test_incorrect_principal_profile_account(self, client, login, token, timezone,
                                                       post_fix="profile_account"):
        await decrease_user()
        data = test_context

        await increase_user()
        await modify_user(login=login, token=token, timezone=timezone)

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.success_ok(Conf.test_client_username)

    async def test_incorrect_cal_ids_profile_account(self, client, post_fix="profile_account"):
        data = test_context

        await increase_user()
        await increase_calendar('invalid_cal_id')

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.success_ok(Conf.test_client_username)

    async def test_exist_profile_account(self, client, post_fix="profile_account"):
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.success_ok(Conf.test_client_username)

    async def test_exist_profile_account_with_notifications(self, client, post_fix="profile_account"):
        data = test_context

        await increase_user()
        await modify_user(e_c=True, ch_stat=True)

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.success_ok(Conf.test_client_username)

    async def test_not_exist_account_update_account(self, client, post_fix="update_account"):
        data = deepcopy(test_context)
        data.update({'values': {
            'login': Conf.test_client_ya_login,
            'token': Conf.test_client_ya_token,
            'timezone': {'value': Conf.test_client_ya_timezone}
        }})

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('login,token,timezone', (
            ("fake_login", 'fake_token', 'UTC'),
            ("invalid_data", 'invalid_data', 'UTC'),
            ('', '', ''),
    ))
    async def test_incorrect_principal_update_account(self, client, login, token, timezone,
                                                      post_fix="update_account"):
        data = deepcopy(test_context)
        data.update({'values': {
            'login': login,
            'token': token,
            'timezone': {'value': timezone}
        }})

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    async def test_success_update_account(self, client, post_fix="update_account"):
        data = deepcopy(test_context)
        data.update({'values': {
            'login': Conf.test_client_ya_login,
            'token': Conf.test_client_ya_token,
            'timezone': {'value': Conf.test_client_ya_timezone}
        }})

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.success_update_integration(Conf.test_client_username)

    async def test_unauth_disconnect_account(self, client, post_fix="disconnect_account"):
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    async def test_success_delete_account_disconnect_account(self, client, post_fix="disconnect_account"):
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.success_remove_integration(Conf.test_client_username)


@pytest.mark.asyncio(scope="module")
class TestChecks:
    endpoint = "/checks/"

    async def test_check_enable_account(self, client, post_fix="check_account"):
        # form
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.is_enable_integration(Conf.test_client_username)

    async def test_check_disable_account(self, client, post_fix="check_account"):
        # form
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.is_disable_integration(Conf.test_client_username)

    async def test_check_enable_scheduler(self, client, post_fix="check_scheduler"):
        await increase_user()
        await increase_calendar(test_calendar1.id)

        # form
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.is_enable_scheduler(Conf.test_client_username)

    async def test_check_disable_scheduler(self, client, post_fix="check_scheduler"):
        # form
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.is_disable_scheduler(Conf.test_client_username)

    async def test_check_fail_check_scheduler_for_unregistered_account(self, client, post_fix="check_scheduler"):
        # form
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)


@pytest.mark.asyncio(scope='module')
class TestCalendar:
    endpoint = '/calendars/'

    async def test_unauth_get_a_week(self, client, post_fix="get_a_week"):
        # form
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_incorrect_principal_get_a_week(self, client, fake_login, fake_token, post_fix="get_a_week"):
        # form
        data = test_context

        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token

        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    async def test_auth_get_a_week(self, client, post_fix="get_a_week"):
        # form
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.success_ok(Conf.test_client_username)

    async def test_unauth_get_a_month(self, client, post_fix="get_a_month"):
        # form
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_incorrect_principal_get_a_month(self, client, fake_login, fake_token, post_fix="get_a_month"):
        # form
        data = test_context

        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token

        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    async def test_auth_get_a_month(self, client, post_fix="get_a_month"):
        # form
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_unauth_from_to(self, client, post_fix="from_to"):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'from_date': '01.01.2023', 'to_date': '02.01.2023'}})

        response = await client.post(self.endpoint + post_fix, json=data)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_incorrect_principal_from_to(self, client, fake_login, fake_token, post_fix="from_to"):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'from_date': '01.01.2023', 'to_date': '02.01.2023'}})

        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token

        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    @pytest.mark.parametrize('from_date, to_date', (
            ('asdasd', 'asdasdasd'),
            ('01.01.999999999', '33.3333.99'),
            ('01.01.22', '01.01.23'),
    ))
    async def test_wrong_format_dates_from_to(self, client, from_date, to_date, post_fix="from_to"):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'from_date': from_date, 'to_date': to_date}})

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.wrong_format_dates_from_to(Conf.test_client_username, from_date,
                                                                          to_date)

    @pytest.mark.parametrize('from_date, to_date', (
            ('01.01.2023', '02.01.2023'),
            ('02.01.2023', '01.01.2023',),
    ))
    async def test_auth_from_to(self, client, from_date, to_date, post_fix='from_to'):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'from_date': from_date, 'to_date': to_date}})

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_unauth_current(self, client, post_fix='current'):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'date': '01.01.2023'}})

        response = await client.post(self.endpoint + post_fix, json=data)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_incorrect_principal_current(self, client, fake_login, fake_token, post_fix='current'):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'date': '01.01.2023'}})

        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token

        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    @pytest.mark.parametrize('dt', (
            ('asdasd'),
            ('01.01.999999999'),
            ('01.01.23'),
    ))
    async def test_wrong_format_date_current(self, client, dt, post_fix='current'):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'date': dt}})

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.wrong_format_date_current(Conf.test_client_username, dt)

    async def test_auth_current(self, client, post_fix='current'):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'date': '01.01.2023'}})

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_unauth_today(self, client, post_fix='today'):
        # form
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)

        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_incorrect_principal_today(self, client, fake_login, fake_token, post_fix='today'):
        # form
        data = test_context

        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token

        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    async def test_auth_today(self, client, post_fix='today'):
        # form
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)

        await decrease_user()

        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'ok'


@pytest.mark.asyncio(scope='module')
class TestNotifications:
    endpoint = '/notifications/'

    async def test_noauth_create_notification(self, client, post_fix='create_notification'):
        # form
        data = test_context
        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_incorrect_principal_create_notification(
            self, client, fake_login, fake_token, post_fix='create_notification'
    ):
        # form
        data = test_context

        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token

        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    async def test_is_exists_scheduler_create_notification(self, client, post_fix='create_notification'):
        data = test_context

        await increase_user()
        await increase_calendar(test_calendar1.id)

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        assert response.status_code == 200
        assert json_response == dict_responses.is_exists_scheduler(Conf.test_client_username)

    async def test_success_create_notification(self, client, post_fix='create_notification'):
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json
        await decrease_user()

        assert response.status_code == 200
        assert json_response['type'] == 'form'

    async def test_noauth_continue_create_notification(self, client, post_fix='continue_create_notification'):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'Calendars': [{'value': test_calendar1.id}, {'value': test_calendar2.id}],
                                "Time": {"value": '7:00'},
                                'Notification': True,
                                'Status': True,
                                }
                     })

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_incorrect_principal_continue_create_notification(
            self, client, fake_login, fake_token, post_fix='continue_create_notification'
    ):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'Calendars': [{'value': test_calendar1.id}, {'value': test_calendar2.id}],
                                "Time": {"value": '7:00'},
                                'Notification': True,
                                'Status': True,
                                }
                     })

        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token

        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    async def test_is_exists_scheduler_continue_create_notification(self, client,
                                                                    post_fix='continue_create_notification'):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'Calendars': [{'value': test_calendar1.id}, {'value': test_calendar2.id}],
                                "Time": {"value": '7:00'},
                                'Notification': True,
                                'Status': True,
                                }
                     })

        await increase_user()
        await increase_calendar(test_calendar1.id)

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        assert response.status_code == 200
        assert json_response == dict_responses.is_exists_scheduler(Conf.test_client_username)

    async def test_success_continue_create_notification(self, client, post_fix='continue_create_notification'):
        data = deepcopy(test_context)
        data.update({'values': {'Calendars': [{'value': test_calendar1.id}, {'value': test_calendar2.id}],
                                "Time": {"value": '7:00'},
                                'Notification': True,
                                'Status': True,
                                }
                     })

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_success_really_update_notification(self, client, post_fix='really_update_notification'):
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'form'

    async def test_noauth_update_notification(self, client, post_fix='update_notification'):
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_incorrect_principal_update_notification(
            self, client, fake_login, fake_token, post_fix='update_notification'
    ):
        data = test_context

        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token

        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    async def test_no_scheduler_update_notification(self, client, post_fix='update_notification'):
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        assert response.status_code == 200
        assert json_response == dict_responses.no_scheduler(Conf.test_client_username)

    async def test_success_update_notification(self, client, post_fix='update_notification'):
        data = test_context

        await increase_user()
        await increase_calendar(test_calendar1.id)

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        assert response.status_code == 200
        assert json_response['type'] == 'form'

    async def test_noauth_continue_update_notification(self, client, post_fix='continue_update_notification'):
        data = deepcopy(test_context)
        data.update({'values': {'Calendars': [{'value': test_calendar1.id}, {'value': test_calendar2.id}],
                                "Time": {"value": '7:00'},
                                'Notification': True,
                                'Status': True,
                                }
                     })

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_incorrect_principal_continue_update_notification(
            self, client, fake_login, fake_token, post_fix='continue_update_notification'
    ):
        # form
        data = deepcopy(test_context)
        data.update({'values': {'Calendars': [{'value': test_calendar1.id}, {'value': test_calendar2.id}],
                                "Time": {"value": '7:00'},
                                'Notification': True,
                                'Status': True,
                                }
                     })

        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token

        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

        assert response.status_code == 200
        assert json_response == dict_responses.incorrect_principal()

    async def test_success_continue_update_notification(self, client, post_fix='continue_update_notification'):
        data = deepcopy(test_context)
        data.update({'values': {'Calendars': [{'value': test_calendar1.id}, {'value': test_calendar2.id}],
                                "Time": {"value": '7:00'},
                                'Notification': True,
                                'Status': True,
                                }
                     })

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        assert response.status_code == 200
        assert json_response['type'] == 'ok'

    async def test_success_really_delete_notification(self, client, post_fix="really_delete_notification"):
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response['type'] == 'form'

    async def test_noauth_delete_notification(self, client, post_fix="delete_notification"):
        data = test_context

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        assert response.status_code == 200
        assert json_response == dict_responses.unauth_integration(Conf.test_client_username)

    async def test_no_scheduler_delete_notification(self, client, post_fix="delete_notification"):
        data = test_context

        await increase_user()

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        assert response.status_code == 200
        assert json_response == dict_responses.no_scheduler(Conf.test_client_username)

    async def test_success_delete_notification(self, client, post_fix="delete_notification"):
        data = test_context

        await increase_user()
        await increase_calendar(test_calendar1.id)

        response = await client.post(self.endpoint + post_fix, json=data)
        json_response = await response.json

        await decrease_user()

        assert response.status_code == 200
        assert json_response == dict_responses.success_remove_scheduler(Conf.test_client_username)


@pytest.mark.asyncio(scope="module")
class TestTasks:
    async def test_task1_noauth(self):
        result = await tasks.daily_notification_job(mm_user_id, *get_h_m_utc("7:00", Conf.test_client_ya_timezone))

        # task1 no auth
        assert result is None

    @pytest.mark.parametrize('fake_login, fake_token', (
            ('incorrect', Conf.test_client_ya_token),
            (Conf.test_client_ya_login, 'incorrect'),
            ('incorrect', 'incorrect'),
    ))
    async def test_task1_incorrect_principal(self, fake_login, fake_token):
        login = Conf.test_client_ya_login
        token = Conf.test_client_ya_token
        Conf.test_client_ya_login = fake_login
        Conf.test_client_ya_token = fake_token

        await increase_user()

        async with get_conn() as conn:
            user = await User.get_user(conn, mm_user_id)

            result = await tasks.daily_notification_job(user.session,
                                                        *get_h_m_utc("7:00", Conf.test_client_ya_timezone))

            assert await User.get_user(conn, mm_user_id) is None
            assert result is None

        Conf.test_client_ya_login = login
        Conf.test_client_ya_token = token

    async def test_task1_no_cals_on_server(self):
        global test_calendar1, test_calendar2

        await increase_user()

        await asyncio.gather(
            increase_calendar(test_calendar1.id),
            increase_calendar(test_calendar2.id),
        )

        await asyncio.gather(
            asyncio.to_thread(test_calendar1.delete),
            asyncio.to_thread(test_calendar2.delete),
        )

        async with get_conn() as conn:
            user = await User.get_user(conn, mm_user_id)
            result = await tasks.daily_notification_job(user.session,
                                                        *get_h_m_utc("7:00", Conf.test_client_ya_timezone))

            assert await YandexCalendar.get_first_cal(conn, mm_user_id) is None
            assert result is None

        await asyncio.gather(
            asyncio.create_task(caldav_create_calendar(test_principal, name=Conf.test_client_calendar_name1)),
            asyncio.create_task(caldav_create_calendar(test_principal, name=Conf.test_client_calendar_name2)),
        )

        test_calendar1, test_calendar2 = await asyncio.gather(
            caldav_calendar_by_name(test_principal, Conf.test_client_calendar_name1),
            caldav_calendar_by_name(test_principal, Conf.test_client_calendar_name2),
        )

        await decrease_user()

    async def test_task1_success(self):
        await increase_user()

        await asyncio.gather(
            increase_calendar(test_calendar1.id),
            increase_calendar(test_calendar2.id),
        )

        async with get_conn() as conn:
            user = await User.get_user(conn, mm_user_id)
            result = await tasks.daily_notification_job(user.session,
                                                        *get_h_m_utc("7:00", Conf.test_client_ya_timezone))
            assert result is None

        await decrease_user()
