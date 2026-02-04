from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from infrastructure.db_helper import DatabaseHelper
from infrastructure.orm.models import WarehouseModel
from services.logger_setup import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class WarehouseMetadataProvider:
    db: DatabaseHelper

    async def get_all(self) -> list[WarehouseModel] | None:
        try:
            async with self.db.session(commit=False) as session:
                res = await session.execute(select(WarehouseModel))
                items = res.scalars().all()
                log.info(f"Successful got warehouses, len={len(items)}")
                return items
        except Exception as e:
            log.error(f"Fail to get warehouses, {e}")
            return None

    async def get_by_id(self, warehouse_id: uuid.UUID) -> WarehouseModel | None:
        try:
            async with self.db.session(commit=False) as session:
                res = await session.execute(
                    select(WarehouseModel).where(WarehouseModel.id == warehouse_id)
                )
                item = res.scalar_one_or_none()
                if item:
                    log.info(f"Successful got warehouse by id={warehouse_id}")
                else:
                    log.info(f"Warehouse not found id={warehouse_id}")
                return item
        except Exception as e:
            log.error(f"Fail to get warehouse id={warehouse_id}, {e}")
            return None

    async def insert(self, data: dict[str, Any], refresh: bool = True) -> WarehouseModel | None:
        try:
            obj = WarehouseModel()
            allowed = set(WarehouseModel.__table__.columns.keys())
            for k, v in data.items():
                if k in ("id", "created_at", "updated_at"):
                    continue
                if k in allowed:
                    setattr(obj, k, v)

            async with self.db.session(commit=True) as session:
                session.add(obj)
                await session.flush()
                if refresh:
                    await session.refresh(obj)

            log.info(f"Warehouse created id={obj.id}")
            return obj
        except IntegrityError as e:
            log.error(f"IntegrityError creating warehouse: {e}")
            return None
        except Exception as e:
            log.error(f"Fail to create warehouse {data}, {e}")
            return None

    async def update_by_id(
        self, warehouse_id: uuid.UUID, patch: dict[str, Any], refresh: bool = True
    ) -> WarehouseModel | None:
        try:
            async with self.db.session(commit=True) as session:
                res = await session.execute(
                    select(WarehouseModel).where(WarehouseModel.id == warehouse_id)
                )
                obj = res.scalar_one_or_none()
                if obj is None:
                    log.info(f"Warehouse not found id={warehouse_id}")
                    return None

                allowed = set(WarehouseModel.__table__.columns.keys())
                for k, v in patch.items():
                    if k in ("id", "created_at", "updated_at"):
                        continue
                    if k in allowed:
                        setattr(obj, k, v)

                await session.flush()
                if refresh:
                    await session.refresh(obj)

                log.info(f"Warehouse updated id={warehouse_id}")
                return obj
        except Exception as e:
            log.error(f"Fail to update warehouse id={warehouse_id}, {e}")
            return None

    async def delete_by_id(self, warehouse_id: uuid.UUID) -> bool:
        """
        Если на складе есть позиции и FK стоит RESTRICT — удаление не даст сделать.
        """
        try:
            async with self.db.session(commit=True) as session:
                res = await session.execute(
                    select(WarehouseModel).where(WarehouseModel.id == warehouse_id)
                )
                obj = res.scalar_one_or_none()
                if obj is None:
                    log.info(f"Warehouse not found id={warehouse_id}")
                    return False

                await session.delete(obj)
                log.info(f"Warehouse deleted id={warehouse_id}")
                return True
        except IntegrityError as e:
            # например FK RESTRICT (warehouse используется в positions)
            log.error(f"IntegrityError deleting warehouse id={warehouse_id}: {e}")
            return False
        except Exception as e:
            log.error(f"Fail to delete warehouse id={warehouse_id}, {e}")
            return False
