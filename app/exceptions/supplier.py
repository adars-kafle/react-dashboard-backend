from fastapi import HTTPException

class SupplierNotFoundException(HTTPException):
    def __init__(self, supplier_id: int):
        super().__init__(status_code=404, detail=f"Supplier with id {supplier_id} not found")

class SupplierAlreadyExistsException(HTTPException):
    def __init__(self, identifier_type: str, value: str):
        super().__init__(
            status_code=400,
            detail=f"Supplier with {identifier_type} '{value}' already exists"
        )
