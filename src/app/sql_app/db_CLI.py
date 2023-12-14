from quart import Quart
import sqlalchemy as sa
import asyncio, click

from ..sql_app.database import metadata_obj, get_conn


def init_app(app: Quart) -> None:
    app.cli.add_command(init_db_command)


@click.command('init-db')
@click.option('--clear', '-c', is_flag=True)
def init_db_command(clear: bool) -> None:
    if clear:
        asyncio.get_event_loop().run_until_complete(_drop_db())
        click.echo('Dropped the database.')

    asyncio.get_event_loop().run_until_complete(_init_db())
    click.echo('Initialized the database.')


async def _init_db():
    async with get_conn() as conn:
        await conn.run_sync(metadata_obj.create_all)


async def _drop_db():
    async with get_conn() as conn:
        stmt = sa.text('DROP TABLE IF EXISTS user_account, yandex_calendar, yandex_conference CASCADE')
        await conn.execute(stmt)
