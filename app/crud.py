from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from .exceptions import SupplierNotFoundException, SupplierAlreadyExistsException, DatabaseOperationException

def get_supplier(db: Session, supplier_id: int):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if supplier is None:
        raise SupplierNotFoundException(supplier_id)
    return supplier

def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Supplier).offset(skip).limit(limit).all()

def create_supplier(db: Session, supplier: schemas.SupplierCreate):
    try:
        db_supplier = models.Supplier(**supplier.dict())
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
    except IntegrityError:
        db.rollback()
        raise SupplierAlreadyExistsException(supplier.email)
    except Exception:
        db.rollback()
        raise DatabaseOperationException("create")

def update_supplier(db: Session, supplier_id: int, supplier: schemas.SupplierUpdate):
    db_supplier = get_supplier(db, supplier_id)
    for key, value in supplier.dict(exclude_unset=True).items():
        setattr(db_supplier, key, value)
    try:
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
    except Exception:
        db.rollback()
        raise DatabaseOperationException("update")

def delete_supplier(db: Session, supplier_id: int):
    db_supplier = get_supplier(db, supplier_id)
    try:
        db.delete(db_supplier)
        db.commit()
        return db_supplier
    except Exception:
        db.rollback()
        raise DatabaseOperationException("delete")