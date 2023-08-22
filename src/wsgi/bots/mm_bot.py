from wsgi.settings import MM_BOT_OPTIONS, MM_APP_TOKEN

import logging, traceback
from mattermostautodriver import Driver
from httpx import HTTPError


def send_msg_client(mm_user_id, msg):
    try:
        bot_create_direct_channel = bot.channels.create_direct_channel(
            [mm_user_id, bot.client.userid]
        )

        bot_create_post = bot.posts.create_post(
            {
                "channel_id": bot_create_direct_channel["id"],
                "message": msg,
            }
        )

    except HTTPError as exp:
        logging.error(
            "Error with mm_user_id=%s. <###traceback###\n%s\n###traceback###>\n\n",
            mm_user_id,
            traceback.format_exc(),
        )


bot = Driver(MM_BOT_OPTIONS)

if MM_APP_TOKEN:
    bot.login()
