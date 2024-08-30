from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import require_auth
from app.db.database import get_db
from app.exceptions.database import DatabaseOperationException
from app.exceptions.supplier import (
    SupplierAlreadyExistsException,
    SupplierNotFoundException,
)
from app.schemas import supplier as supplier_schema
from app.schemas.user import User
from app.services.supplier_service import SupplierService

routes = APIRouter()


@routes.get("/", response_model=list[supplier_schema.Supplier])
async def get_suppliers(
    current_user: User = Depends(require_auth),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return SupplierService.get_suppliers(db, skip, limit)


@routes.get("/{supplier_id}", response_model=supplier_schema.Supplier)
async def get_supplier(
    supplier_id: UUID,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    try:
        return SupplierService.get_supplier(db, supplier_id)
    except SupplierNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@routes.post("/", response_model=supplier_schema.Supplier)
async def create_supplier(
    supplier: supplier_schema.SupplierCreate,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    try:
        return SupplierService.create_supplier(db=db, supplier=supplier)
    except SupplierAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@routes.put("/{supplier_id}", response_model=supplier_schema.Supplier)
async def update_supplier(
    supplier_id: UUID,
    supplier: supplier_schema.SupplierUpdate,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    try:
        return SupplierService.update_supplier(
            db=db, supplier_id=supplier_id, supplier=supplier
        )
    except SupplierNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@routes.delete("/{supplier_id}", status_code=204)
async def delete_supplier(
    supplier_id: UUID,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    try:
        SupplierService.delete_supplier(db=db, supplier_id=supplier_id)
    except SupplierNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
