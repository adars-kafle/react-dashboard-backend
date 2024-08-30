from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.db.database import get_db
from app.config.settings import settings_config
from app.services.user_service import UserService
from app.schemas.user import Token, User, UserCreate, UserLogin
from app.exceptions.user import UserNotFoundException, UserAlreadyExistsException
from app.exceptions.database import DatabaseOperationException

routes = APIRouter()

@routes.post("/login", response_model=Token)
async def login(form_data: UserLogin, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = UserService.authenticate_user(db=db, email=form_data.email, password=form_data.password)
        access_token = security.create_access_token(
            data={"sub": user.email},
            expires_delta=settings_config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return {"access_token": access_token, "token_type": "bearer"}
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
