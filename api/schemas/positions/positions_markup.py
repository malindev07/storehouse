from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class PositionsMarkupFilter(BaseModel):
    category: Optional[str] = None
    sub_category: Optional[str] = None
    warehouse_id: Optional[UUID] = None
    ids: Optional[list[UUID]] = None


class PositionsMarkupUpdateRequest(BaseModel):
    percent: float = Field(..., ge=-95, le=500)  # скидка до -95%, наценка до +500%
    filter: PositionsMarkupFilter
