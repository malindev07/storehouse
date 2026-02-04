from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Any, Optional

from api.dependencies import get_positions_use_cases, get_update_positions_markup_uc
from api.schemas.positions.positions import PositionRead, PositionCreate, PositionUpdate
from api.schemas.positions.positions_markup import (
    PositionsMarkupUpdateRequest,
    PositionsMarkupFilter,
)
from use_cases.position import PositionsUseCases
from uuid import UUID

from use_cases.positions_markup import UpdatePositionsMarkupUseCase

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("", response_model=list[PositionRead])
async def list_positions(
    warehouse_id: Optional[UUID] = Query(default=None),
    category: Optional[str] = Query(default=None),
    sub_category: Optional[str] = Query(default=None),
    uc: PositionsUseCases = Depends(get_positions_use_cases),
):
    items = await uc.search(
        warehouse_id=warehouse_id,
        category=category,
        sub_category=sub_category,
    )
    return [x.to_dict() for x in items]


@router.get("/{position_id}", response_model=PositionRead)
async def get_position(
    position_id: UUID, uc: PositionsUseCases = Depends(get_positions_use_cases)
):
    item = await uc.get_position(position_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return item.to_dict()


@router.post("", response_model=PositionRead, status_code=201)
async def create_position(
    body: PositionCreate, uc: PositionsUseCases = Depends(get_positions_use_cases)
):
    item = await uc.create_position(body.model_dump())
    if item is None:
        raise HTTPException(status_code=400, detail="Failed to create position")
    return item.to_dict()


@router.post("/bulk", status_code=200)
async def create_positions_bulk(
    bodies: list[PositionCreate],
    uc: PositionsUseCases = Depends(get_positions_use_cases),
):
    payload = [b.model_dump() for b in bodies]
    result = await uc.create_many(payload)
    if result is None:
        raise HTTPException(status_code=400, detail="Bulk insert failed")
    ok, failed = result
    return {
        "ok": [x.to_dict() for x in ok],
        "failed": [{"item": it, "error": err} for it, err in failed],
    }


@router.patch("/{position_id}", response_model=PositionRead)
async def update_position(
    position_id: str,
    body: PositionUpdate,
    uc: PositionsUseCases = Depends(get_positions_use_cases),
):
    patch = body.model_dump(exclude_unset=True)
    item = await uc.update_position(position_id, patch)
    if item is None:
        raise HTTPException(
            status_code=404, detail="Position not found or update failed"
        )
    return item.to_dict()


@router.patch("/bulk", status_code=200)
async def update_positions_bulk(
    ids_data: dict[str, dict[str, Any]],
    uc: PositionsUseCases = Depends(get_positions_use_cases),
):
    updated, failed = await uc.update_many(ids_data)
    return {
        "updated": [x.to_dict() for x in updated],
        "failed": [{"id": pid, "error": err} for pid, err in failed],
    }


@router.delete("/{position_id}", status_code=204)
async def delete_position(
    position_id: str, uc: PositionsUseCases = Depends(get_positions_use_cases)
):
    ok = await uc.delete_position(position_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Position not found")
    return None


@router.post("/delete-bulk", status_code=200)
async def delete_positions_bulk(
    ids: list[str], uc: PositionsUseCases = Depends(get_positions_use_cases)
):
    await uc.delete_many(ids)
    return {"deleted_ids": ids}


@router.patch("/markup-percent", status_code=200)
async def apply_markup_percent(
    body: PositionsMarkupUpdateRequest,
    uc: UpdatePositionsMarkupUseCase = Depends(get_update_positions_markup_uc),
):
    try:
        updated = await uc.execute(
            percent=body.percent,
            category=body.filter.category,
            sub_category=body.filter.sub_category,
            warehouse_id=body.filter.warehouse_id,
            ids=body.filter.ids,
        )
        return {"updated": updated, "percent": body.percent}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
