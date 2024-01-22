import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

from ..settings import Conf

engine = create_async_engine(Conf.DB_URL)#, echo=True if Conf.LOG_LEVEL == 10 else None)
metadata_obj = sa.MetaData()


# Dependency
def get_conn():
    conn = engine.begin()
    return conn
