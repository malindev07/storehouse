from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from infrastructure.orm.metadata_providers.positionsMetadataProvider import (
    PositionsMetadataProvider,
)


@dataclass(slots=True)
class UpdatePositionsMarkupUseCase:
    positions: PositionsMetadataProvider

    async def execute(
        self,
        *,
        percent: float,
        category: str | None = None,
        sub_category: str | None = None,
        warehouse_id: UUID | None = None,
        ids: list[UUID] | None = None,
    ) -> int:
        # защита от "обнулить всё" и от невалидного фактора
        factor = 1.0 + (percent / 100.0)
        if factor <= 0:
            raise ValueError("percent too small: factor must be > 0")

        if not any([category, sub_category, warehouse_id, ids]):
            raise ValueError("At least one filter must be provided")

        return await self.positions.apply_markup_percent_by_filter(
            percent=percent,
            category=category,
            sub_category=sub_category,
            warehouse_id=warehouse_id,
            ids=ids,
        )
