from wsgi.settings import DB_URL

from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine

engine = create_engine(DB_URL, echo=True)

metadata_obj = MetaData()


class User:
    user_table = Table(

        "user_account", metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", String, nullable=False, unique=True),
        Column("login", String, nullable=False, unique=True),
        Column("token", String, nullable=False, unique=True),
        Column("timezone", String, nullable=False),

    )

    @classmethod
    def add_user(cls, user_id: str, login: str, token: str, timezone: str):
        with engine.begin() as connection:
            c = cls.user_table.columns

            result = connection.execute(
                cls.user_table
                .insert()
                .returning(c.id, c.user_id, c.login, c.token, c.timezone),
                {'user_id': user_id, 'login': login, 'token': token, 'timezone': timezone}
            )

        return result.first()

    @classmethod
    def get_user(cls, user_id: str):
        with engine.connect() as connection:
            c = cls.user_table.columns

            result = connection.execute(
                cls.user_table
                .select()
                .where(c.user_id == user_id)
            )

        return result.first()

    @classmethod
    def remove_user(cls, user_id: str):
        with engine.begin() as connection:
            c = cls.user_table.columns

            result = connection.execute(
                cls.user_table
                .delete()
                .where(c.user_id == user_id)
                .returning(c.id, c.user_id, c.login, c.token, c.timezone)
            )

        return result.first()

    @classmethod
    def update_user(cls, user_id: str, login: str, token: str, timezone: str):
        with engine.begin() as connection:
            c = cls.user_table.columns

            result = connection.execute(
                cls.user_table
                .update()
                .where(c.user_id == user_id)
                .values(login=login, token=token, timezone=timezone)
                .returning(c.id, c.user_id, c.login, c.token, c.timezone)
            )

        return result.first()

    def __init__(self, user_id: str, login: str, token: str, timezone: str):
        self.user_id = user_id
        self.login = login
        self.token = token
        self.timezone = timezone

    def save(self):
        return User.add_user(self.user_id, self.login, self.token, self.timezone)
