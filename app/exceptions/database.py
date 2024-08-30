from fastapi import HTTPException

class DatabaseOperationException(HTTPException):
    def __init__(self, operation: str, details: str):
        super().__init__(status_code=500, detail=f"Database operation failed: {operation}. Details: {details}")
