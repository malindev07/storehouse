from __future__ import annotations

from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ProviderManagerCreate(BaseModel):
    provider_id: UUID
    telephones: str
    name: str


class ProviderManagerUpdate(BaseModel):
    telephones: Optional[str] = None
    name: Optional[str] = None


class ProviderManagerRead(BaseModel):
    id: UUID
    provider_id: UUID
    telephones: str
    name: str
