from __future__ import annotations

from typing import Any
from uuid import UUID

from infrastructure.orm.metadata_providers.warehouseMetadataProvider import WarehouseMetadataProvider
from infrastructure.orm.models import WarehouseModel


class WarehousesUseCases:
    def __init__(self, warehouses: WarehouseMetadataProvider):
        self.warehouses = warehouses

    async def list(self) -> list[WarehouseModel]:
        res = await self.warehouses.get_all()
        return res or []

    async def get(self, warehouse_id: UUID) -> WarehouseModel | None:
        return await self.warehouses.get_by_id(warehouse_id)

    async def create(self, data: dict[str, Any]) -> WarehouseModel | None:
        return await self.warehouses.insert(data, refresh=True)

    async def update(self, warehouse_id: UUID, patch: dict[str, Any]) -> WarehouseModel | None:
        return await self.warehouses.update_by_id(warehouse_id, patch, refresh=True)

    async def delete(self, warehouse_id: UUID) -> bool:
        return await self.warehouses.delete_by_id(warehouse_id)
