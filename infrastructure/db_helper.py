import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from infrastructure.orm.models.base import Base
from infrastructure.orm.settings import Settings


class DatabaseHelper:
    def __init__(self, db_url: str, db_echo: bool = False):
        self.engine = create_async_engine(
            url=db_url,
            echo=db_echo,
            pool_pre_ping=True,  # Автоматическая проверка соединения
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    async def session(self) -> AsyncGenerator[AsyncSession, Exception]:
        try:
            async with self.session_factory() as session:
                yield session
        except Exception as e:
            raise e

    @asynccontextmanager
    async def session(self, *, commit: bool = True) -> AsyncIterator[AsyncSession]:
        """
        commit=True  -> commit на успешный выход, rollback на ошибку
        commit=False -> только rollback на ошибку (удобно для readonly операций)
        """
        async with self.session_factory() as session:
            try:
                yield session
                if commit:
                    await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def health_check(self) -> bool:
        """Проверка доступности БД"""
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            raise e

    async def recreate_all(self) -> None:
        async with self.engine.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.drop_all)
            except Exception as e:
                raise e
            finally:
                print("DB dropped all")
            try:
                await conn.run_sync(Base.metadata.create_all)
            except Exception:
                raise
            finally:
                print("DB created all")


url = Settings().database_url
db_helper = DatabaseHelper(db_url=url)
# asyncio.run(db_helper.recreate_all())
