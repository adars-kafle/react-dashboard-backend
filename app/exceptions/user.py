from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int | str):
        super().__init__(
            status_code=404, detail=f"User with id or email '{user_id}' not found"
        )


class UserAlreadyExistsException(HTTPException):
    def __init__(self, field: str, value: str):
        super().__init__(
            status_code=400, detail=f"User with {field} '{value}' already exists"
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid email or password")
