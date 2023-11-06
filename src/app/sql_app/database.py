from contextlib import asynccontextmanager
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

from app.settings import envs

engine = create_async_engine(envs.DB_URL, echo=True if envs.DEBUG else None)
metadata_obj = MetaData()


@asynccontextmanager
async def get_conn():
    async with engine.begin() as conn:
        yield conn
