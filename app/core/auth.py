from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config.settings import settings_config
from app.db.database import get_db
from app.schemas.user import TokenPayload, User
from app.services.user_service import UserService

# Define OAuth2PasswordBearer with the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    access_token: str = Cookie(None, alias="access_token"),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not access_token:
        raise credentials_exception

    try:
        token = access_token.replace("Bearer ", "")
        payload = jwt.decode(
            token, settings_config.SECRET_KEY, algorithms=[settings_config.ALGORITHM]
        )
        email: str | None = payload.get("sub")
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
