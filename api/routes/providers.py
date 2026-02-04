from __future__ import annotations

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from api.dependencies import get_provider_use_cases
from api.schemas.provider_managers import ProviderManagerCreate
from api.schemas.providers import ProviderRead, ProviderUpdate, ProviderCreate
from use_cases.providers import ProviderUseCases

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=list[ProviderRead])
async def list_providers(uc: ProviderUseCases = Depends(get_provider_use_cases)):
    providers = await uc.list_providers()
    return [p.to_dict() for p in providers]


@router.get("/{provider_id}", response_model=ProviderRead)
async def get_provider(provider_id: UUID, uc: ProviderUseCases = Depends(get_provider_use_cases)):
    p = await uc.get_provider(provider_id)
    if not p:
        raise HTTPException(status_code=404, detail="Provider not found")
    return p.to_dict()


@router.post("", response_model=ProviderRead, status_code=201)
async def create_provider(body: ProviderCreate, uc: ProviderUseCases = Depends(get_provider_use_cases)):
    try:
        p = await uc.create_provider(body.model_dump())
        return p.to_dict()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Provider conflict")


@router.patch("/{provider_id}", response_model=ProviderRead)
async def update_provider(provider_id: UUID, body: ProviderUpdate, uc: ProviderUseCases = Depends(get_provider_use_cases)):
    patch = body.model_dump(exclude_unset=True)
    p = await uc.update_provider(provider_id, patch)
    if not p:
        raise HTTPException(status_code=404, detail="Provider not found")
    return p.to_dict()


@router.delete("/{provider_id}", status_code=204)
async def delete_provider(provider_id: UUID, uc: ProviderUseCases = Depends(get_provider_use_cases)):
    ok = await uc.delete_provider(provider_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Provider not found")
    return None


# бизнес-эндпоинт: создать provider + manager
@router.post("/with-manager", response_model=ProviderRead, status_code=201)
async def create_provider_with_manager(
    provider: ProviderCreate,
    manager: ProviderManagerCreate,
    uc: ProviderUseCases = Depends(get_provider_use_cases),
):
    # manager.provider_id в этом сценарии можно игнорировать и назначать автоматически,
    # но оставлю как есть — если хочешь, сделаем отдельную схему без provider_id.
    p = await uc.create_provider_with_manager(provider.model_dump(), manager.model_dump())
    return p.to_dict()
