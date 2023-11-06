import caldav, asyncio
from caldav import Principal
import caldav.lib.error as caldav_errors


async def take_principal(login, token) -> Principal | dict:
    url = f'https://{login}:{token}@caldav.yandex.ru'

    try:
        with caldav.DAVClient(url=url) as client:
            principal = await asyncio.to_thread(client.principal)

    except caldav_errors.AuthorizationError as exp:

        principal = {
            'type': 'error',
            'text': 'Incorrect username or token. Possible, you changed the username and password'
        }

    except caldav_errors.DAVError as exp:

        principal = {
            'type': 'error',
            'text': 'Unknown Error. Please, contact with your admin platform.'
        }

    return principal
