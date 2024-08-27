from pydantic import BaseModel

class SupplierBase(BaseModel):
    name: str
    contact_info: str
    address: str

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        orm_mode = True