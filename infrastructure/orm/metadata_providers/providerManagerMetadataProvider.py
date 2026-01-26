from dataclasses import dataclass
from typing import Any
import uuid

from sqlalchemy import select, delete, func

from infrastructure.db_helper import DatabaseHelper
from infrastructure.orm.models import ProviderManagerModel


@dataclass(slots=True)
class ProviderManagerMetadataProvider:
    db: DatabaseHelper

    async def get_all(self) -> list[ProviderManagerModel]:
        async with self.db.session(commit=False) as session:
            res = await session.execute(select(ProviderManagerModel))
            return res.scalars().all()

    async def get_by_id(self, manager_id: uuid.UUID) -> ProviderManagerModel | None:
        async with self.db.session(commit=False) as session:
            res = await session.execute(
                select(ProviderManagerModel).where(
                    ProviderManagerModel.id == manager_id
                )
            )
            return res.scalar_one_or_none()

    async def get_by_provider_id(
        self, provider_id: uuid.UUID
    ) -> list[ProviderManagerModel]:
        async with self.db.session(commit=False) as session:
            res = await session.execute(
                select(ProviderManagerModel).where(
                    ProviderManagerModel.provider_id == provider_id
                )
            )
            return res.scalars().all()

    async def insert(
        self, data: dict[str, Any], *, refresh: bool = True
    ) -> ProviderManagerModel:
        obj = ProviderManagerModel(**data)

        async with self.db.session(commit=True) as session:
            session.add(obj)
            await session.flush()
            if refresh:
                await session.refresh(obj)
            return obj

    async def update_by_id(
        self,
        manager_id: uuid.UUID,
        patch: dict[str, Any],
        *,
        refresh: bool = True,
    ) -> ProviderManagerModel | None:
        async with self.db.session(commit=True) as session:
            res = await session.execute(
                select(ProviderManagerModel).where(
                    ProviderManagerModel.id == manager_id
                )
            )
            obj = res.scalar_one_or_none()
            if obj is None:
                return None

            allowed = set(ProviderManagerModel.__table__.columns.keys())
            for k, v in patch.items():
                if k in ("id", "created_at", "updated_at"):
                    continue
                # provider_id лучше менять отдельным методом/правилом, но если хочешь — оставь:
                if k in allowed:
                    setattr(obj, k, v)

            obj.updated_at = func.now()

            await session.flush()
            if refresh:
                await session.refresh(obj)
            return obj

    async def delete_by_id(self, manager_id: uuid.UUID) -> bool:
        async with self.db.session(commit=True) as session:
            res = await session.execute(
                select(ProviderManagerModel).where(
                    ProviderManagerModel.id == manager_id
                )
            )
            obj = res.scalar_one_or_none()
            if obj is None:
                return False
            await session.delete(obj)
            return True

    async def delete_many_by_ids(self, ids: list[uuid.UUID]) -> int:
        if not ids:
            return 0
        async with self.db.session(commit=True) as session:
            result = await session.execute(
                delete(ProviderManagerModel).where(ProviderManagerModel.id.in_(ids))
            )
            return result.rowcount or 0
