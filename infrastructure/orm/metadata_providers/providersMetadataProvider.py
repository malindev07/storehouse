from dataclasses import dataclass
from typing import Any
import uuid

from sqlalchemy import select, delete, update, func
from sqlalchemy.orm import selectinload

from infrastructure.db_helper import DatabaseHelper
from infrastructure.orm.models import ProviderModel, ProviderManagerModel


@dataclass(slots=True)
class ProviderMetadataProvider:
    db: DatabaseHelper

    async def get_all(self) -> list[ProviderModel]:
        async with self.db.session(commit=False) as session:
            res = await session.execute(
                select(ProviderModel).options(selectinload(ProviderModel.managers))
            )
            return res.scalars().all()

    async def get_by_id(self, provider_id: uuid.UUID) -> ProviderModel | None:
        async with self.db.session(commit=False) as session:
            res = await session.execute(
                select(ProviderModel)
                .where(ProviderModel.id == provider_id)
                .options(selectinload(ProviderModel.managers))
            )
            return res.scalar_one_or_none()

    async def insert(
        self, data: dict[str, Any], *, refresh: bool = True
    ) -> ProviderModel:
        obj = ProviderModel(**data)

        async with self.db.session(commit=True) as session:
            session.add(obj)
            await session.flush()
            if refresh:
                await session.refresh(obj)
            return obj

    async def update_by_id(
        self,
        provider_id: uuid.UUID,
        patch: dict[str, Any],
        *,
        refresh: bool = True,
    ) -> ProviderModel | None:
        async with self.db.session(commit=True) as session:
            res = await session.execute(
                select(ProviderModel).where(ProviderModel.id == provider_id)
            )
            obj = res.scalar_one_or_none()
            if obj is None:
                return None

            allowed = set(ProviderModel.__table__.columns.keys())
            for k, v in patch.items():
                if k in ("id", "created_at", "updated_at"):
                    continue
                if k in allowed:
                    setattr(obj, k, v)

            # гарантируем updated_at
            obj.updated_at = func.now()

            await session.flush()
            if refresh:
                await session.refresh(obj)
            return obj

    async def delete_by_id(self, provider_id: uuid.UUID) -> bool:
        """
        Если на Provider есть ссылки (positions/provider_manager) и стоит RESTRICT — удаление не пройдёт.
        """
        async with self.db.session(commit=True) as session:
            res = await session.execute(
                select(ProviderModel).where(ProviderModel.id == provider_id)
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
                delete(ProviderModel).where(ProviderModel.id.in_(ids))
            )
            return result.rowcount or 0

    async def create_with_manager(
        self,
        provider_data: dict[str, Any],
        manager_data: dict[str, Any],
        *,
        refresh: bool = True,
    ) -> ProviderModel:
        """
        Создать поставщика + одного менеджера в ОДНОЙ транзакции.
        (так выполняем правило “у поставщика всегда есть карточка менеджера”)
        """
        provider = ProviderModel(**provider_data)

        async with self.db.session(commit=True) as session:
            session.add(provider)
            await session.flush()  # получаем provider.id (uuid уже есть, но flush безопасен)

            manager = ProviderManagerModel(**manager_data, provider_id=provider.id)
            session.add(manager)

            await session.flush()
            if refresh:
                await session.refresh(provider)
                # если хочешь сразу подтянуть managers:
                await session.refresh(manager)

            return provider
