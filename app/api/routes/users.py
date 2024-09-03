from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import require_auth
from app.db.database import get_db
from app.exceptions.database import DatabaseOperationException
from app.exceptions.user import UserNotFoundException
from app.schemas.user import User, UserUpdate
from app.services.user_service import UserService

routes = APIRouter()


@routes.get("/me", response_model=User)
async def get_user(current_user: User = Depends(require_auth)):
    return current_user


@routes.put("/me", response_model=User)
async def update_user(
    new_data: UserUpdate,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db),
):
    try:
        updated_user = UserService.update_user(
            db=db, user_id=current_user.id, user=new_data
        )
        return updated_user
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    except DatabaseOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}",
        )
