import json
from typing import Any, List, Optional
from loguru import logger

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session


from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.ItemOut])
def read_itemss(
    request: Request,
    db: Session = Depends(deps.get_db),
    after_field: str = "doh_code",
    after_value: Any = None,
    limit: int = 500,
) -> Any:
    """
    Retrieve item information.
    """
    results = crud.item.get_multi(
        db, limit=limit, after_field=after_field, after_value=after_value
    )

    return results


# @router.post("/", response_model=schemas.Item)
# def create_hospital(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_superuser),
#     hospital_in: schemas.ItemCreate,
# ) -> Any:
#     """
#     Create new hospital.
#     """
#     hospital = crud.hospital.get_by_name(db, name=hospital_in.name)
#     if hospital:
#         raise HTTPException(
#             status_code=400,
#             detail="The hospital with this name already exists in the system.",
#         )
#     hospital = crud.hospital.create(db, obj_in=hospital_in)
#     return hospital


@router.get("/{doh_code}", response_model=schemas.Item)
def read_hospital_by_id(
    doh_code: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific hospital by doh_code.
    """
    hospital = crud.hospital.get_by_doh_code(db, doh_code=doh_code)
    if not hospital:
        raise HTTPException(status_code=404, detail="Item not found")
    logger.debug(f"Item {hospital}")
    logger.debug(f"Schema {schemas.Item.from_orm(hospital)}")
    return hospital


@router.put("/{doh_code}", response_model=schemas.Item)
async def update_hospital(
    *,
    db: Session = Depends(deps.get_db),
    doh_code: str,
    hospital_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a hospital.
    """
    logger.debug(f"current_user {current_user}")
    hospital = crud.hospital.get_by_doh_code(db, doh_code=doh_code)
    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="The hospital with this id does not exist in the system",
        )

    hospital = crud.hospital.update(db, db_obj=hospital, obj_in=hospital_in)
    data = schemas.Item.from_orm(hospital).json()
    await deps.sse_notify(**{"event": "update:hospital", "data": data})

    return hospital
