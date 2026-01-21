import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from infrastructure.orm.models import PositionsModel


from infrastructure.db_helper import DatabaseHelper
from services.logger_setup import get_logger

log = get_logger(__name__)


@dataclass
class PositionsMetadataProvider:
    db: DatabaseHelper

    async def get_all(self) -> list[PositionsModel] | None:
        try:
            async with self.db.session(commit=True) as session:
                query = select(PositionsModel)
                result = await session.execute(query)
                scalar_result = result.scalars().all()
                log.info(msg=f"Successful got list items, len = {len(scalar_result)}")
                return scalar_result
        except Exception as e:
            log.info(msg=f"Fail to get items, {e}")
            return None

    async def get_by_id(self, position_id: str):
        try:
            async with self.db.session(commit=True) as session:
                query = select(PositionsModel).where(PositionsModel.id == position_id)
                result = await session.execute(query)
                scalar_result = result.scalar_one_or_none()
                log.info(msg=f"Successful got item by id {position_id}")
                log.debug(
                    msg=f"Successful got item by id {position_id}, item - {scalar_result.to_dict()}"
                )
                return scalar_result
        except Exception as e:
            log.info(msg=f"Fail to get item with id {position_id}, {e}")
            return None

    async def insert_many(self, items: list[Any], refresh: bool = False):
        ok: list[PositionsModel] = []
        failed: list[tuple[Any, str]] = []
        try:
            for item in items:
                obj = (
                    item
                    if isinstance(item, PositionsModel)
                    else PositionsModel.from_dict(item)
                )

                try:
                    async with self.db.session(commit=True) as session:
                        session.add(obj)
                        await session.flush()
                        if refresh:
                            await session.refresh(obj)
                    ok.append(obj)

                except IntegrityError as e:
                    # этот obj не сохранился, но остальные продолжим
                    failed.append((item, str(e.orig)))

            return ok, failed
        except Exception as e:
            log.debug(msg=(ok, failed))
            log.info(msg=f"Fail to insert items, {e}")

    async def insert(
        self, item: dict[str, Any] | PositionsModel, refresh: bool = True
    ) -> PositionsModel | None:

        try:
            obj = (
                item
                if isinstance(item, PositionsModel)
                else PositionsModel.from_dict(item)
            )
            async with self.db.session() as session:
                session.add(obj)
                # чтобы obj гарантированно получил PK/дефолты до refresh
                await session.flush()
                if refresh:
                    await session.refresh(obj)
                return obj
        except Exception as e:
            log.info(msg=f"Fail to insert {item}, {e}")
            return None

    def delete_many(self):
        pass

    def delete(self):
        pass

    def update_many(self):
        pass

    def update(self):
        pass


# 1) вставить одну
