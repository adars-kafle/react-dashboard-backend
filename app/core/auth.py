from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.schemas.user import TokenPayload, User
from app.services.user_service import UserService
from app.config.settings import settings_config
from app.db.database import get_db

# Define OAuth2PasswordBearer with the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token! Please login!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings_config.SECRET_KEY, algorithms=[settings_config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenPayload(sub=email)
    except JWTError:
        raise credentials_exception

    user = UserService.get_user_by_email(db=db, email=token_data.sub)
    if user is None:
        raise credentials_exception

    return user

def require_auth(current_user: User = Depends(get_current_user)):
    return current_user
