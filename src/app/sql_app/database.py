from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from settings import Conf

engine = create_async_engine(Conf.DB_URL, echo=True if Conf.DEBUG else None)
metadata_obj = MetaData()


# Dependency
def get_conn():
    conn = engine.begin()
    return conn
