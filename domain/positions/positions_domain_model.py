from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass
class PositionCreate:
    category: str
    sub_category: str
    name: str
    description: str
    balance: int
    min_balance: int
    purchase_price: float
    markup: float
    warehouse_id: UUID
    provider_id: Optional[UUID] = None
    sale_price: float | None = field(default=None)
