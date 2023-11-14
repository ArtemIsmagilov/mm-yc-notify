import caldav, asyncio
from caldav import Principal
import caldav.lib.error as caldav_errors

from ..dict_responses import incorrect_principal, dav_error


async def take_principal(login, token) -> Principal | dict:
    url = f'https://{login}:{token}@caldav.yandex.ru'

    try:
        with caldav.DAVClient(url=url) as client:
            principal = await asyncio.to_thread(client.principal)

    except caldav_errors.AuthorizationError as exp:

        principal = incorrect_principal()

    except caldav_errors.DAVError as exp:

        principal = dav_error()

    return principal
