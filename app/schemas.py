from pydantic import BaseModel, EmailStr

class SupplierBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    phone: str

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    phone: str | None = None

class Supplier(SupplierBase):
    id: int

    class Config:
        orm_mode = True