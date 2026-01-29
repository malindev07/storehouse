from __future__ import annotations

from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class PositionCreate(BaseModel):
    category: str
    sub_category: str
    name: str
    description: str
    balance: Optional[int] = None
    min_balance: Optional[int] = None
    purchase_price: float
    sale_price: float
    markup: float

    provider_id: Optional[UUID] = None
    provider_manager_id: Optional[UUID] = None


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

    provider_id: Optional[UUID] = None
    provider_manager_id: Optional[UUID] = None


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

    provider_id: Optional[UUID] = None
    provider_manager_id: Optional[UUID] = None
