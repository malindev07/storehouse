from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from uuid import UUID
from api.dependencies import get_manager_use_cases
from api.schemas.provider_managers import ProviderManagerRead, ProviderManagerCreate, ProviderManagerUpdate
from use_cases.provider_managers import ProviderManagerUseCases

router = APIRouter(prefix="/managers", tags=["provider_managers"])


@router.get("", response_model=list[ProviderManagerRead])
async def list_managers(uc: ProviderManagerUseCases = Depends(get_manager_use_cases)):
    managers = await uc.list_managers()
    return [m.to_dict() for m in managers]


@router.get("/{manager_id}", response_model=ProviderManagerRead)
async def get_manager(manager_id: UUID, uc: ProviderManagerUseCases = Depends(get_manager_use_cases)):
    m = await uc.get_manager(manager_id)
    if not m:
        raise HTTPException(status_code=404, detail="Manager not found")
    return m.to_dict()


@router.get("/by-provider/{provider_id}", response_model=list[ProviderManagerRead])
async def list_managers_by_provider(provider_id: UUID, uc: ProviderManagerUseCases = Depends(get_manager_use_cases)):
    managers = await uc.list_by_provider(provider_id)
    return [m.to_dict() for m in managers]


@router.post("", response_model=ProviderManagerRead, status_code=201)
async def create_manager(body: ProviderManagerCreate, uc: ProviderManagerUseCases = Depends(get_manager_use_cases)):
    m = await uc.create_manager(body.model_dump())
    return m.to_dict()


@router.patch("/{manager_id}", response_model=ProviderManagerRead)
async def update_manager(manager_id: UUID, body: ProviderManagerUpdate, uc: ProviderManagerUseCases = Depends(get_manager_use_cases)):
    patch = body.model_dump(exclude_unset=True)
    m = await uc.update_manager(manager_id, patch)
    if not m:
        raise HTTPException(status_code=404, detail="Manager not found")
    return m.to_dict()


@router.delete("/{manager_id}", status_code=204)
async def delete_manager(manager_id: UUID, uc: ProviderManagerUseCases = Depends(get_manager_use_cases)):
    ok = await uc.delete_manager(manager_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Manager not found")
    return None
