from __future__ import annotations

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ProviderCreate(BaseModel):
    name: str
    address: str
    description: str


class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None


class ProviderRead(BaseModel):
    id: UUID
    name: str
    address: str
    description: str
