from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import AsyncIterator, Any

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
    AsyncSession)

from src.constants.env import DB_URL
from src.utils.json_handler import json_serialize

class __DatabaseSessionManager:
    """
    A database session manager help manage multiple database engine easier than top-level definition
    """
    def __init__(self, url: str, **engine_kwargs: Any) -> None:
        self._engine = create_async_engine(url, **engine_kwargs)
        self._session_maker = async_sessionmaker(bind=self._engine, expire_on_commit=True)

    @asynccontextmanager
    async def _get_connection(self) -> AsyncIterator[AsyncConnection]:
        """Create and retrieve a database connection. Use to test database migration"""
        if self._engine is None:
            raise Exception("Database session manager is not initialized")
        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception as e:
                await conn.rollback()
                raise e

    @asynccontextmanager
    async def aget_session(self) -> AsyncIterator[AsyncSession]:
        """Create and retrieve a database session"""
        if self._session_maker is None:
            raise Exception("Database session manager is not initialized")
        async with self._session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e

    async def aclose_connections(self) -> None:
        """Close all database connections"""
        if self._engine is None:
            raise Exception("Database session manager is not initialized")

        await self._engine.dispose()

        self._engine = None
        self._session_maker = None

DATABASE_MANAGER = __DatabaseSessionManager(
    DB_URL,
    pool_size=5,
    max_overflow=10,  # max_overflow + pool_size = max size = 15
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,  # Phát hiện và loại bỏ kết nối chết,
    json_serializer=json_serialize)

async def aget_db() -> AsyncGenerator[AsyncSession]:
    """Retrieve a database session"""
    async with DATABASE_MANAGER.aget_session() as session:
        yield session
