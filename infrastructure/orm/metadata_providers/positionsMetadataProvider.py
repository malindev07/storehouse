import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Any

from sqlalchemy import select, update, and_
from sqlalchemy.exc import IntegrityError

from infrastructure.orm.models import PositionsModel


from infrastructure.db_helper import DatabaseHelper
from services.logger_setup import get_logger

log = get_logger(__name__)
from uuid import UUID


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

    async def get_by_id(self, position_id: UUID) -> PositionsModel | None:
        try:
            async with self.db.session(commit=True) as session:
                query = select(PositionsModel).where(PositionsModel.id == position_id)
                result = await session.execute(query)
                position = result.scalar_one_or_none()
                log.info(msg=f"Successful got item by id {position_id}")
                log.debug(
                    msg=f"Successful got item by id {position_id}, item - {position.to_dict()}"
                )
                return position
        except Exception as e:
            log.info(msg=f"Fail to get item with id {position_id}, {e}")
            return None

    async def insert_many(
        self, items: list[Any], refresh: bool = False
    ) -> tuple | None:
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
                    return None

            return ok, failed
        except Exception as e:
            log.debug(msg=(ok, failed))
            log.info(msg=f"Fail to insert items, {e}")
            return None

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

    async def delete_many(self, positions_id: list[str]):
        if not positions_id:
            return False

        async with self.db.session() as session:
            try:
                query = select(PositionsModel).where(
                    PositionsModel.id.in_(positions_id)
                )
                result = await session.execute(query)
                positions = result.scalars().all()

                for position in positions:
                    try:
                        await session.delete(position)
                        log.info(
                            msg=f"Position id - {position.id} successfully deleted"
                        )
                    except Exception as e:
                        log.info(msg=f"Position id - {position.id} can not delete, {e}")
            except Exception as e:
                log.error(msg=f"Fail to delete, {e}")

    async def delete_by_id(self, position_id: str) -> bool:
        try:
            async with self.db.session() as session:
                query = select(PositionsModel).where(PositionsModel.id == position_id)
                result = await session.execute(query)
                position = result.scalar_one_or_none()
                if position is None:
                    log.info(msg=f"Position with id {position_id} is not found")
                    return False
                await session.delete(position)
                log.info(msg=f"Position with id {position_id} successfully deleted")
                return True
        except Exception as e:
            log.error(msg=f"Fail to delete id - {position_id}, {e}")
            return False

    async def update_many_by_id(
        self, ids_data: dict[str, dict[str, Any]]
    ) -> tuple[list[PositionsModel], list[tuple[str, str]]]:
        updated: list[PositionsModel] = []
        failed: list[tuple[str, str]] = []

        allowed = set(PositionsModel.__table__.columns.keys())

        try:
            async with self.db.session(commit=True) as session:
                # 1) Забираем все записи одним запросом
                res = await session.execute(
                    select(PositionsModel).where(
                        PositionsModel.id.in_(list(ids_data.keys()))
                    )
                )
                positions = res.scalars().all()

                found_ids = {p.id for p in positions}
                # 2) То, чего нет в БД — сразу в failed
                for pid in ids_data.keys():
                    if pid not in found_ids:
                        failed.append((pid, "NOT_FOUND"))

                # 3) Обновляем каждую запись отдельно, чтобы ошибка не откатывала всех
                for position in positions:
                    pid = position.id
                    patch = ids_data.get(pid, {})

                    try:
                        async with session.begin_nested():  # SAVEPOINT
                            for k, v in patch.items():
                                if k in ("id", "created_at", "updated_at"):
                                    continue
                                if k in allowed:
                                    setattr(position, k, v)
                            await session.flush()
                        await session.refresh(position)
                        updated.append(position)
                        log.info(f"Position id={pid} successfully updated")

                    except IntegrityError as e:
                        failed.append((pid, f"INTEGRITY_ERROR: {e.orig}"))
                        log.warning(f"Position id={pid} update failed: {e}")
                    except Exception as e:
                        failed.append((pid, str(e)))
                        log.error(f"Position id={pid} update failed: {e}")

            return updated, failed

        except Exception as e:
            log.error(f"Error to update positions {list(ids_data.keys())}, {e}")
            # если упало вообще всё (например, нет соединения) — логично вернуть всех как failed
            return [], [(pid, f"DB_ERROR: {e}") for pid in ids_data.keys()]

    async def update_by_id(
        self, position_id: str, data: dict[str, Any]
    ) -> PositionsModel | None:

        try:
            async with self.db.session(commit=True) as session:
                res = await session.execute(
                    select(PositionsModel).where(PositionsModel.id == position_id)
                )
                position = res.scalar_one_or_none()
                if position is None:
                    return None

                allowed = set(PositionsModel.__table__.columns.keys())
                for k, v in data.items():
                    if k in ("id", "created_at", "updated_at"):
                        continue
                    if k in allowed:
                        setattr(position, k, v)

                await session.flush()
                await session.refresh(position)

                log.info(msg=f"Position id - {position_id} successfully update")
                return position
        except Exception as e:
            log.error(msg=f"Error to update position id - {position_id}, {e}")
            return None

    async def get_by_category(self, category: str) -> list[PositionsModel] | None:
        try:
            async with self.db.session(commit=False) as session:
                q = select(PositionsModel).where(PositionsModel.category == category)
                res = await session.execute(q)
                items = res.scalars().all()
                log.info(f"Got positions by category='{category}', len={len(items)}")
                return items
        except Exception as e:
            log.error(f"Fail get_by_category '{category}': {e}")
            return None

    async def get_by_sub_category(
        self, sub_category: str
    ) -> list[PositionsModel] | None:
        try:
            async with self.db.session(commit=False) as session:
                q = select(PositionsModel).where(
                    PositionsModel.sub_category == sub_category
                )
                res = await session.execute(q)
                items = res.scalars().all()
                log.info(
                    f"Got positions by sub_category='{sub_category}', len={len(items)}"
                )
                return items
        except Exception as e:
            log.error(f"Fail get_by_sub_category '{sub_category}': {e}")
            return None

    async def apply_markup_percent_by_filter(
        self,
        *,
        percent: float,
        category: str | None = None,
        sub_category: str | None = None,
        warehouse_id: UUID | None = None,
        ids: list[UUID] | None = None,
    ) -> int:
        factor = 1.0 + (percent / 100.0)

        if factor <= 0:
            raise ValueError("percent results in non-positive factor")

        conditions = []
        if category is not None:
            conditions.append(PositionsModel.category == category)
        if sub_category is not None:
            conditions.append(PositionsModel.sub_category == sub_category)
        if warehouse_id is not None:
            conditions.append(PositionsModel.warehouse_id == warehouse_id)
        if ids:
            conditions.append(PositionsModel.id.in_(ids))

        if not conditions:
            raise ValueError("At least one filter must be provided")

        async with self.db.session(commit=True) as session:
            stmt = (
                update(PositionsModel)
                .where(and_(*conditions))
                .values(markup=PositionsModel.markup * factor)
                .execution_options(synchronize_session="fetch")
            )
            res = await session.execute(stmt)
            return int(res.rowcount or 0)

    async def search(
        self,
        *,
        warehouse_id: Optional[UUID] = None,
        category: Optional[str] = None,
        sub_category: Optional[str] = None,
    ) -> list[PositionsModel] | None:
        try:
            async with self.db.session(commit=False) as session:
                q = select(PositionsModel)

                if warehouse_id is not None:
                    q = q.where(PositionsModel.warehouse_id == warehouse_id)
                if category is not None:
                    q = q.where(PositionsModel.category == category)
                if sub_category is not None:
                    q = q.where(PositionsModel.sub_category == sub_category)

                res = await session.execute(q)
                items = res.scalars().all()
                log.info(
                    f"Positions search: warehouse_id={warehouse_id}, category={category}, "
                    f"sub_category={sub_category}, len={len(items)}"
                )
                return items
        except Exception as e:
            log.error(f"Fail to search positions: {e}")
            return None
