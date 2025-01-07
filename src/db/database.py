from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
    AsyncSession)


class DatabaseSessionManager:
    def __init__(self, url: str, **engine_kwargs: Any):
        """
            A database session manager help manage multiple database engine easier than top-level definition
            :param url: Database connection string
            :param engine_kwargs: Keyword arguments used for engine configuration
        """
        self._engine = create_async_engine(url, **engine_kwargs)
        self._session_maker = async_sessionmaker(bind=self._engine)

    @asynccontextmanager
    async def _get_connection(self):
        """Create and retrieve a database connection. Use to test database migration"""
        if self._engine is None:
            raise ValueError("Database session manager is not initialized")
        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception as e:
                await conn.rollback()
                raise e

    @asynccontextmanager
    async def aget_session(self):
        """Create and retrieve a database session"""
        if self._session_maker is None:
            raise ValueError("Database session manager is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.aclose()

    async def aclose_connections(self):
        """Close all database connections"""
        if self._engine is None:
            raise ValueError("Database session manager is not initialized")

        await self._engine.dispose()

        self._engine = None
        self._session_maker = None

    @property
    def engine(self):
        if not self._engine:
            raise ValueError("Database session manager is not initialized")
        return self._engine
