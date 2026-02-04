from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class PositionCreate(BaseModel):
    category: str
    sub_category: str
    name: str
    description: str
    balance: Optional[int] = None
    min_balance: Optional[int] = None
    purchase_price: float
    markup: float

    warehouse_id: UUID  # <-- обязательно
    provider_id: Optional[UUID] = None


class PositionUpdate(BaseModel):
    category: Optional[str] = None
    sub_category: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    balance: Optional[int] = None
    min_balance: Optional[int] = None
    purchase_price: Optional[float] = None
    sale_price: Optional[float] = None
    markup: Optional[float] = None

    warehouse_id: Optional[UUID] = None
    provider_id: Optional[UUID] = None


class PositionRead(BaseModel):
    id: UUID
    category: str
    sub_category: str
    name: str
    description: str
    balance: Optional[int] = None
    min_balance: Optional[int] = None
    purchase_price: float
    sale_price: float
    markup: float

    warehouse_id: UUID  # <-- в ответе
    provider_id: Optional[UUID] = None
