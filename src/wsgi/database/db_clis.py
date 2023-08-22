from wsgi.database.models import metadata_obj, engine

from sqlalchemy import text


def init_db() -> None:
    metadata_obj.create_all(engine)


def drop_db() -> None:
    with engine.begin() as connection:
        stmt = text(
            "DROP TABLE IF EXISTS apscheduler_job, user_account, yandex_calendar, yandex_conference CASCADE;"
        )

        connection.execute(stmt)
