from __future__ import annotations

from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class WarehouseCreate(BaseModel):
    name: str
    address: str


class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None


class WarehouseRead(BaseModel):
    id: UUID
    name: str
    address: str
