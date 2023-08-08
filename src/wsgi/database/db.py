from wsgi.database.models import User, metadata_obj, engine, SCHEDULER_CONF

import click


def init_db():
    metadata_obj.create_all(engine)


@click.command('init-db')
@click.option('--clear', '-c', is_flag=True)
def init_db_command(clear: bool):
    if clear:
        metadata_obj.drop_all(engine)

    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)
    # app.cli.add_command(add_some_commands)
