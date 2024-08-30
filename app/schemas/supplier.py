from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class SupplierBase(BaseModel):
    name: str
    email: EmailStr
    address: str
    phone: str

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class Supplier(SupplierBase):
    id: UUID

    class Config:
        from_attributes = True
