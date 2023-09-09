from wsgi.settings import envs

import logging, traceback
from mattermostautodriver import Driver
from httpx import HTTPError


def decorator_http_error(func):
    def wrapper(*args, **kwargs):
        try:

            return func(*args, **kwargs)

        except HTTPError as exp:

            logging.error("<###traceback###\n%s\n###traceback###>\n\n", traceback.format_exc())

            return exp

    return wrapper


@decorator_http_error
def send_msg_client(mm_user_id, msg):
    bot_create_direct_channel = bot.channels.create_direct_channel([mm_user_id, bot.client.userid])

    return bot.posts.create_post(
        {
            "channel_id": bot_create_direct_channel["id"],
            "message": msg,
        }
    )


@decorator_http_error
def update_custom_status(mm_user_id: str, new_options: dict):
    return bot.status.update_user_custom_status(mm_user_id, new_options)


@decorator_http_error
def get_user_by_username(username: str):
    return bot.users.get_user_by_username(username)


@decorator_http_error
def create_user(options: dict):
    return bot.users.create_user(options)


bot = Driver(envs.MM_BOT_OPTIONS)

if envs.MM_APP_TOKEN:
    bot.login()
