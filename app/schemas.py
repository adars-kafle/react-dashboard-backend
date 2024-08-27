from pydantic import BaseModel

class SupplierBase(BaseModel):
    name: str
    email: str
    address: str
    phone: str

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        orm_mode = True