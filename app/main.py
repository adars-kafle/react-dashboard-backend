from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db
from .exceptions import SupplierNotFoundException, SupplierAlreadyExistsException, DatabaseOperationException

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create a new supplier
@app.post("/suppliers/", response_model=schemas.Supplier)
def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_supplier(db=db, supplier=supplier)
    except SupplierAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# Get the list of suppliers
@app.get("/suppliers/", response_model=list[schemas.Supplier])
def read_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    suppliers = crud.get_suppliers(db, skip=skip, limit=limit)
    return suppliers

# Get supplier by ID
@app.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_supplier(db, supplier_id=supplier_id)
    except SupplierNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# Update a specific supplier
@app.put("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def update_supplier(supplier_id: int, supplier: schemas.SupplierUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_supplier(db, supplier_id=supplier_id, supplier=supplier)
    except SupplierNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# Delete a specific supplier
@app.delete("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_supplier(db, supplier_id=supplier_id)
    except SupplierNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)