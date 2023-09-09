from sqlalchemy.engine import Row
from flask import Request


def check_user(user: Row, request: Request) -> dict:
    mm_username = request.json['context']['acting_user']['username']

    if user:

        return {
            'type': 'ok',
            'text': f'# @{mm_username}, your integration with Yandex Calendar is enable :)',
        }

    else:

        return {
            'type': 'ok',
            'text': (f'# @{mm_username}, your integration with Yandex Calendar is disable :(\n'
                     'You need complete connect to integration.'),
        }
