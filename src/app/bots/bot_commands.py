import asyncio

from ..settings import envs
from ..decorators.account_decorators import bot_error

from mattermostautodriver import AsyncDriver

bot = AsyncDriver(envs.MM_BOT_OPTIONS)

if envs.MM_APP_TOKEN:
    asyncio.get_event_loop().run_until_complete(bot.login())


@bot_error
async def send_msg_client(mm_user_id, msg, props=None):
    bot_create_direct_channel = await bot.channels.create_direct_channel([mm_user_id, bot.client.userid])
    data = {"channel_id": bot_create_direct_channel["id"], "message": msg, }

    if props:
        data.update({"props": props, })

    return await bot.posts.create_post(data)


@bot_error
async def update_custom_status(mm_user_id: str, new_options: dict):
    return await bot.status.update_user_custom_status(mm_user_id, new_options)


@bot_error
async def get_user_by_username(username: str):
    return await bot.users.get_user_by_username(username)


@bot_error
async def get_user_by_mm_user_id(mm_user_id: str):
    return await bot.users.get_user(mm_user_id)


@bot_error
async def create_user(options: dict):
    return await bot.users.create_user(options)
