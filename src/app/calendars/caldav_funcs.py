import caldav
import caldav.lib.error as caldav_errors
from caldav import Principal

from ..async_wraps.async_wrap_caldav import caldav_principal
from ..dict_responses import (
    incorrect_principal,
    dav_error
)


async def take_principal(login: str, token: str) -> Principal | dict:
    url = f'https://{login}:{token}@caldav.yandex.ru'

    try:
        with caldav.DAVClient(url=url) as client:
            principal = await caldav_principal(client)

    except caldav_errors.AuthorizationError as exp:

        principal = incorrect_principal()

    except caldav_errors.DAVError as exp:

        principal = dav_error()

    return principal
