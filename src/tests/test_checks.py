from wsgi.database import db
from wsgi.settings import envs
from wsgi.schedulers import sd
from tests.conftest import mm_user_id, mm_username

from datetime import datetime, UTC, timedelta


class TestChecks:

    def test_check_enable_account(self, client):
        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}}

        # create test_user connection
        db.User.add_user(mm_user_id, envs.test_client_ya_login, envs.test_client_ya_token, envs.test_client_ya_timezone,
                         e_c=False, ch_stat=False)

        response = client.post('/checks/check_account', json=data)

        # delete testuser after connection
        db.User.remove_user(mm_user_id)

        assert response.json == {'type': 'ok',
                                 'text': f'# @{mm_username}, your integration with Yandex Calendar is enable :)',
                                 }

    def test_check_disable_account(self, client):
        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}}

        response = client.post('/checks/check_account', json=data)

        assert response.json == {'type': 'ok',
                                 'text': (f'# @{mm_username}, your integration with Yandex Calendar is disable :(\n'
                                          'You need complete connect to integration.'),
                                 }

    def test_check_enable_scheduler(self, client):
        # create test_user connection
        db.User.add_user(mm_user_id, envs.test_client_ya_login, envs.test_client_ya_token, envs.test_client_ya_timezone,
                         e_c=False, ch_stat=False)

        # existed testuser's job
        job_id = f'{mm_user_id}(test_job)'
        test_job = sd.scheduler.add_job(
            func=print,
            trigger='date',
            args=('hi',),
            id=job_id,
            name=mm_username,
            replace_existing=True,
            run_date=datetime.now(UTC) + timedelta(days=365)
        )

        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}}

        response = client.post('/checks/check_scheduler', json=data)

        test_job.remove()

        # delete testuser after connection
        db.User.remove_user(mm_user_id)

        assert response.json == {'type': 'ok', 'text': '# Your scheduler is enable :)'}

    def test_check_disable_scheduler(self, client):
        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}}

        # create test_user connection
        db.User.add_user(mm_user_id, envs.test_client_ya_login, envs.test_client_ya_token, envs.test_client_ya_timezone,
                         e_c=False, ch_stat=False)

        response = client.post('/checks/check_scheduler', json=data)

        # delete testuser after connection
        db.User.remove_user(mm_user_id)

        assert response.json == {'type': 'ok', 'text': '# You don\'t have scheduler notifications :('}

    def test_check_fail_check_scheduler_for_unregistered_account(self, client):
        # form
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}}

        response = client.post('/checks/check_scheduler', json=data)

        assert response.json == {'type': 'error',
                                 'text': 'Your haven\'t integration with yandex-calendar. First, to connect'
                                 }
