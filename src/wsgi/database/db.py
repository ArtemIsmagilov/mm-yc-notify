from wsgi.database import db_clis
from wsgi.database.models import User, YandexCalendar, YandexConference
import click


@click.command('init-db')
@click.option('--clear', '-c', is_flag=True)
def init_db_command(clear: bool) -> None:
    if clear:
        db_clis.drop_db()
        click.echo('dropped the database.')

    db_clis.init_db()
    click.echo('Initialized the database.')


def init_app(app) -> None:
    app.cli.add_command(init_db_command)
    # app.cli.add_command(add_some_commands)
