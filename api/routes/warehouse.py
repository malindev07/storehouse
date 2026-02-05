from __future__ import annotations

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_warehouses_usecases, get_positions_use_cases
from api.schemas.positions.positions import PositionReadSchema
from api.schemas.warehouse import WarehouseRead, WarehouseCreate, WarehouseUpdate
from use_cases.position import PositionsUseCases
from use_cases.warehouse import WarehousesUseCases

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.get("", response_model=list[WarehouseRead])
async def list_warehouses(uc: WarehousesUseCases = Depends(get_warehouses_usecases)):
    items = await uc.list()
    return [x.to_dict() for x in items]


@router.get("/{warehouse_id}", response_model=WarehouseRead)
async def get_warehouse(
    warehouse_id: UUID, uc: WarehousesUseCases = Depends(get_warehouses_usecases)
):
    item = await uc.get(warehouse_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return item.to_dict()


@router.post("", response_model=WarehouseRead, status_code=201)
async def create_warehouse(
    body: WarehouseCreate, uc: WarehousesUseCases = Depends(get_warehouses_usecases)
):
    item = await uc.create(body.model_dump())
    if item is None:
        raise HTTPException(status_code=400, detail="Failed to create warehouse")
    return item.to_dict()


@router.patch("/{warehouse_id}", response_model=WarehouseRead)
async def update_warehouse(
    warehouse_id: UUID,
    body: WarehouseUpdate,
    uc: WarehousesUseCases = Depends(get_warehouses_usecases),
):
    patch = body.model_dump(exclude_unset=True)
    item = await uc.update(warehouse_id, patch)
    if item is None:
        raise HTTPException(
            status_code=404, detail="Warehouse not found or update failed"
        )
    return item.to_dict()


@router.delete("/{warehouse_id}", status_code=204)
async def delete_warehouse(
    warehouse_id: UUID, uc: WarehousesUseCases = Depends(get_warehouses_usecases)
):
    ok = await uc.delete(warehouse_id)
    if not ok:
        # часто тут будет 409 если склад используется позициями (FK RESTRICT)
        raise HTTPException(
            status_code=400,
            detail="Failed to delete warehouse (maybe used by positions)",
        )
    return None


@router.get("/{warehouse_id}/positions", response_model=list[PositionReadSchema])
async def list_positions_in_warehouse(
    warehouse_id: UUID,
    uc: PositionsUseCases = Depends(get_positions_use_cases),
):
    items = await uc.search(warehouse_id=warehouse_id)
    return [x.to_dict() for x in items]
