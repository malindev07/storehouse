from __future__ import annotations

from typing import Any

from infrastructure.orm.metadata_providers.positionsMetadataProvider import PositionsMetadataProvider
from infrastructure.orm.models import PositionsModel
from uuid import UUID

class PositionsUseCases:
    def __init__(self, positions: PositionsMetadataProvider):
        self.positions = positions

    async def list_positions(self) -> list[PositionsModel]:
        res = await self.positions.get_all()
        return res or []

    async def get_position(self, position_id: UUID) -> PositionsModel | None:
        return await self.positions.get_by_id(position_id)

    async def create_position(self, data: dict[str, Any]) -> PositionsModel | None:
        return await self.positions.insert(data, refresh=True)

    async def create_many(self, items: list[dict[str, Any]]):
        # вернёт (ok, failed) или None
        return await self.positions.insert_many(items, refresh=False)

    async def update_position(self, position_id: str, patch: dict[str, Any]) -> PositionsModel | None:
        return await self.positions.update_by_id(position_id, patch)

    async def update_many(self, ids_data: dict[str, dict[str, Any]]):
        # вернёт (updated, failed)
        return await self.positions.update_many_by_id(ids_data)

    async def delete_position(self, position_id: str) -> bool:
        return await self.positions.delete_by_id(position_id)

    async def delete_many(self, ids: list[str]) -> bool:
        await self.positions.delete_many(ids)
        return True
