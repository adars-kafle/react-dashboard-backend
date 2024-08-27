from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello world!"}

# Create a supplier
@app.post("/suppliers/", response_model=schemas.Supplier)
def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return crud.create_supplier(db=db, supplier=supplier)

# Get the list of all suppliers
@app.get("/suppliers/", response_model=list[schemas.Supplier])
def read_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    suppliers = crud.get_suppliers(db, skip=skip, limit=limit)
    return suppliers

# Get supplier by ID
@app.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

# Update a supplier
@app.put("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def update_supplier(supplier_id: int, supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = crud.update_supplier(db, supplier_id=supplier_id, supplier=supplier)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

# Delete a supplier
@app.delete("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = crud.delete_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier