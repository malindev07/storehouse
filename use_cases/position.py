from __future__ import annotations

from typing import Any, Optional

from api.schemas.positions.positions import PositionCreateSchema
from domain.positions.positions import PositionDomain
from infrastructure.orm.metadata_providers.positionsMetadataProvider import (
    PositionsMetadataProvider,
)
from infrastructure.orm.models import PositionsModel
from uuid import UUID

from services.logger_setup import get_logger
from use_cases.converters.positions import PositionConverter
from use_cases.response import UseCaseResponse

logger = get_logger(__name__)


class PositionsUseCases:
    def __init__(self, positions: PositionsMetadataProvider):
        self.positions = positions
        self.domain = PositionDomain()
        self.converter = PositionConverter()

    async def list_positions(self) -> list[PositionsModel]:
        res = await self.positions.get_all()
        return res or []

    async def get_position(self, position_id: UUID) -> PositionsModel | None:
        return await self.positions.get_by_id(position_id)

    async def create_position(self, schema: PositionCreateSchema) -> UseCaseResponse:
        position = await self.domain.create(
            await self.converter.create_schema_to_domain(schema)
        )
        if position is not None:
            model = await self.converter.create_domain_to_model(position)
            result = await self.positions.insert(model, refresh=True)
            if result is not None:
                params = await self.converter.create_model_to_schema(model)

                return UseCaseResponse(
                    success=True,
                    msg=f"Model created successfully",
                    params=params,
                )

        return UseCaseResponse(
            success=False,
            msg=f"Model created failed",
            params=schema.model_dump(),
        )

    async def create_many(self, items: list[dict[str, Any]]):
        # вернёт (ok, failed) или None
        return await self.positions.insert_many(items, refresh=False)

    async def update_position(
        self, position_id: str, patch: dict[str, Any]
    ) -> PositionsModel | None:
        return await self.positions.update_by_id(position_id, patch)

    async def update_many(self, ids_data: dict[str, dict[str, Any]]):
        # вернёт (updated, failed)
        return await self.positions.update_many_by_id(ids_data)

    async def delete_position(self, position_id: str) -> bool:
        return await self.positions.delete_by_id(position_id)

    async def delete_many(self, ids: list[str]) -> bool:
        await self.positions.delete_many(ids)
        return True

    async def find_by_category(self, category: str):
        res = await self.positions.get_by_category(category)
        return res or []

    async def find_by_sub_category(self, sub_category: str):
        res = await self.positions.get_by_sub_category(sub_category)
        return res or []

    async def search(
        self,
        *,
        warehouse_id: Optional[UUID] = None,
        category: Optional[str] = None,
        sub_category: Optional[str] = None,
    ):
        res = await self.positions.search(
            warehouse_id=warehouse_id,
            category=category,
            sub_category=sub_category,
        )
        return res or []
