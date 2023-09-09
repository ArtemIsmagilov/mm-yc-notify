from wsgi.converters import create_table_md
from wsgi.settings import envs
from wsgi.database import db
from tests.conftest import mm_user_id, mm_username

import pytest


class TestConnections:

    @pytest.mark.parametrize('login,token,timezone', (
            ("fake_login", 'fake_token', 'UTC'),
            ("invalid_data", 'invalid_data', 'UTC'),
            ('', '', ''),
    ))
    def test_fail_connect_account(self, client, login, token, timezone):
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}},
                # mattermost form data
                'values': {'login': login,
                           'token': token,
                           'timezone': {'value': timezone},
                           }
                }

        response = client.post("/connections/connect_account", json=data)

        assert response.json == {'type': 'error',
                                 'text': 'Incorrect username or token. Possible, you changed the username and password'
                                 }

    def test_fail_connect_for_exist_account(self, client):
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}},
                # mattermost form data
                'values': {'login': envs.test_client_ya_login,
                           'token': envs.test_client_ya_token,
                           'timezone': {'value': envs.test_client_ya_timezone},
                           }
                }

        # create test_user connection
        db.User.add_user(mm_user_id, envs.test_client_ya_login, envs.test_client_ya_token, envs.test_client_ya_timezone,
                         e_c=False, ch_stat=False)

        response = client.post("/connections/connect_account", json=data)

        # delete testuser after connection
        db.User.remove_user(mm_user_id)

        assert response.json == {'type': 'error', 'text': 'Your integration with yandex-calendar already exists.'}

    def test_success_connect_account(self, client):
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}},
                # mattermost form data
                'values': {'login': envs.test_client_ya_login,
                           'token': envs.test_client_ya_token,
                           'timezone': {'value': envs.test_client_ya_timezone},
                           }
                }

        response = client.post("/connections/connect_account", json=data)

        msg = {
            'type': 'ok',
            'text': f'@{mm_username}, you successfully CREATE integration with yandex calendar'
        }

        # delete testuser after connection
        db.User.remove_user(mm_user_id)

        assert response.json == msg

    def test_anonymous_profile_account(self, client):
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}}

        response = client.post("/connections/profile_account", json=data)

        text = create_table_md({'status': 'Anonymous'})

        assert response.json == {'type': 'ok', 'text': text}

    def test_exist_profile_account(self, client):
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}, }

        # create test_user connection
        db.User.add_user(mm_user_id, envs.test_client_ya_login, envs.test_client_ya_token, envs.test_client_ya_timezone,
                         e_c=False, ch_stat=False)

        # show me profile
        response = client.post("/connections/profile_account", json=data)

        text = create_table_md({
            'status': 'User',
            'login': envs.test_client_ya_login,
            'username': f'@{mm_username}',
            'timezone': envs.test_client_ya_timezone,
            'notify_every_confernece': str(False),
            'changing_status_every_confernece': str(False),
            'sync_calendars': str(None),
        })

        # delete test user after connection
        db.User.remove_user(mm_user_id)

        assert response.json == {'type': 'ok', 'text': text}

    def test_fail_update_for_not_exist_account(self, client):
        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}},
                # mattermost form data
                'values': {'login': envs.test_client_ya_login,
                           'token': envs.test_client_ya_token,
                           'timezone': {'value': envs.test_client_ya_timezone},
                           }
                }

        response = client.post("/connections/update_account", json=data)

        assert response.json == {'type': 'error',
                                 'text': 'Your haven\'t integration with yandex-calendar. First, to connect'
                                 }

    @pytest.mark.parametrize('login,token,timezone', (
            ("fake_login", 'fake_token', 'UTC'),
            ("invalid_data", 'invalid_data', 'UTC'),
            ('', '', ''),
    ))
    def test_fail_update_account(self, client, login, token, timezone):
        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}},
                # mattermost form data
                'values': {'login': login,
                           'token': token,
                           'timezone': {'value': timezone},
                           }
                }
        # create test_user connection
        db.User.add_user(mm_user_id, envs.test_client_ya_login, envs.test_client_ya_token, envs.test_client_ya_timezone,
                         e_c=False, ch_stat=False)

        response = client.post("/connections/update_account", json=data)

        # delete testuser after connection
        db.User.remove_user(mm_user_id)

        assert response.json == {'type': 'error',
                                 'text': 'Incorrect username or token. Possible, you changed the username and password'
                                 }

    def test_success_update_account(self, client):
        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}},
                # mattermost form data
                'values': {'login': envs.test_client_ya_login,
                           'token': envs.test_client_ya_token,
                           'timezone': {'value': envs.test_client_ya_timezone},
                           }
                }
        # create test_user connection
        db.User.add_user(mm_user_id, envs.test_client_ya_login, envs.test_client_ya_token, envs.test_client_ya_timezone,
                         e_c=False, ch_stat=False)

        response = client.post("/connections/update_account", json=data)

        # delete testuser after connection
        db.User.remove_user(mm_user_id)

        assert response.json == {'type': 'ok',
                                 'text': (f'@{mm_username}, you successfully UPDATE integration with yandex calendar. '
                                          'Your scheduler notifications was deleted if is existed')
                                 }

    def test_fail_delete_for_not_exist_account(self, client):
        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}}

        response = client.post("/connections/disconnect_account", json=data)

        assert response.json == {'type': 'error',
                                 'text': 'Your haven\'t integration with yandex-calendar. First, to connect'}

    def test_success_delete_account(self, client):
        # create test_user connection
        db.User.add_user(mm_user_id, envs.test_client_ya_login, envs.test_client_ya_token, envs.test_client_ya_timezone,
                         e_c=False, ch_stat=False)

        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}}

        response = client.post("/connections/disconnect_account", json=data)

        # delete testuser after connection
        db.User.remove_user(mm_user_id)

        assert response.json == {'type': 'ok',
                                 'text': (f'@{mm_username}, you successfully REMOVE integration with yandex calendar. '
                                          'Your scheduler notifications was deleted if is existed.')
                                 }
