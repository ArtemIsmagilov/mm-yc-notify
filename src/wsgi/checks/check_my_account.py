from sqlalchemy.engine import Row


def check_user(user: Row) -> dict:
    if user:

        return {
            'type': 'ok',
            'text': '# Your integration with Yandex Calendar is enable :)',
        }

    else:

        return {
            'type': 'ok',
            'text': '# Your integration with Yandex Calendar is disable :(\n You need complete connect to integration.',
        }
