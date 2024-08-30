from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.settings import settings_config
from app.core import security
from app.db.database import get_db
from app.exceptions.database import DatabaseOperationException
from app.exceptions.user import UserAlreadyExistsException, UserNotFoundException
from app.schemas.user import Token, User, UserCreate, UserLogin
from app.services.user_service import UserService

routes = APIRouter()


@routes.post("/login", response_model=Token)
async def login(
    response: Response, form_data: UserLogin, db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = UserService.authenticate_user(
            db=db, email=form_data.email, password=form_data.password
        )
        access_token = security.create_access_token(
            data={"sub": user.email},
            expires_delta=settings_config.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        # Set the access token in a secure HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings_config.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        return {"message": "User logged in successfully!"}
    except (UserNotFoundException, ValueError):
        raise credentials_exception


@routes.post("/signup", response_model=User)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = UserService.create_user(db=db, user=user)
        return new_user
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@routes.post("/logout", response_model=Token)
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "User logged out successfully!"}
