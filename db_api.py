import asyncio

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker
import contextlib
import os
from schema import Base


def _get_connection_url() -> str:
    user = os.getenv("POSTGRES_USER", "sqlalchemy")
    pwd = os.getenv("POSTGRES_PASSWORD", "sqlalchemy")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv('POSTGRES_DEFAULT_DATABASE', 'sqlalchemy')
    return f"postgresql+asyncpg://{user}:{pwd}@{host}:{port}/{database}"


@contextlib.asynccontextmanager
async def async_session():

    conn_url = _get_connection_url()
    engine = create_async_engine(
        conn_url,
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_sessionmaker() as session:
        # async with session.begin() as session:
        yield session
