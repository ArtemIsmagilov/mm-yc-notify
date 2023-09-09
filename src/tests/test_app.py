from tests.conftest import mm_user_id, mm_username


class TestApp:

    def test_help_info(self, client):
        data = {'context': {'acting_user': {'id': mm_user_id, 'username': mm_username}}}

        response = client.post('/help_info', json=data)

        text = open('tests/test_templates/test_info.md').read()

        assert response.json == {'type': 'ok', 'text': text}
