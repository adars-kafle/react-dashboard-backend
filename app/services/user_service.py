from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.db import db_models
from app.exceptions.database import DatabaseOperationException
from app.exceptions.user import UserAlreadyExistsException, UserNotFoundException
from app.schemas import user as user_schema


class UserService:
    @staticmethod
    def get_user(db: Session, user_id: UUID) -> user_schema.User:
        """
        Get a user by ID

        Args:
            db (Session): The database session
            user_id (int): The ID of the user to retrieve

        Returns:
            user_schema.User: The user with the given ID

        Raises:
            UserNotFoundException: If the user with the given ID is not found
        """
        user = db.query(db_models.User).filter_by(id=user_id).first()
        if user is None:
            raise UserNotFoundException(user_id)
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> user_schema.User:
        """
        Get a user by email

        Args:
            db (Session): The database session
            email (str): The email of the user to retrieve

        Returns:
            user_schema.User: The user with the given email
        """
        return db.query(db_models.User).filter_by(email=email).first()

    @staticmethod
    def get_users(
        db: Session, skip: int = 0, limit: int = 100
    ) -> list[user_schema.User]:
        """
        Get all users

        Args:
            db (Session): The database session
            skip (int): Number of users to skip
            limit (int): Maximum number of users to return

        Returns:
            list[user_schema.User]: A list of users
        """
        users = db.query(db_models.User).offset(skip).limit(limit).all()
        return users

    @staticmethod
    def create_user(db: Session, user: user_schema.UserCreate) -> user_schema.User:
        """
        Create a new user

        Args:
            db (Session): The database session
            user (user_schema.UserCreate): The user data to store/create

        Returns:
            user_schema.User: The newly created user

        Raises:
            UserAlreadyExistsException: If a user with the same email already exists
            DatabaseOperationException: If the database operation fails
        """
        # Check if user already exists
        existing_user = db.query(db_models.User).filter_by(email=user.email).first()
        if existing_user:
            raise UserAlreadyExistsException("email", user.email)

        # If not, create the new user
        hashed_password = get_password_hash(user.password)
        new_user = db_models.User(
            name=user.name, email=user.email, hashed_password=hashed_password
        )
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                "create_user", f"Integrity error: {str(e)}"
            )
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(
                "create_user", f"Unexpected error: {str(e)}"
            )

    @staticmethod
    def update_user(
        db: Session, user_id: UUID, user: user_schema.UserUpdate
    ) -> user_schema.User:
        """
        Update a user by ID

        Args:
            db (Session): The database session
            user_id (int): The ID of the user to update
            user (user_schema.UserUpdate): The updated user data

        Returns:
            user_schema.User: The updated user

        Raises:
            UserNotFoundException: If the user with the given ID is not found
            DatabaseOperationException: If the database operation fails
        """
        existing_user = db.query(db_models.User).filter_by(id=user_id).first()
        if existing_user is None:
            raise UserNotFoundException(f"User with ID {user_id} not found!")

        # Update the user data if exists
        update_data = user.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )
        for key, value in update_data.items():
            setattr(existing_user, key, value)

        try:
            db.commit()
            db.refresh(existing_user)
            return existing_user
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                "update_user", f"Integrity error: {str(e)}"
            )
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(
                "update_user", f"Unexpected error: {str(e)}"
            )

    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> None:
        """
        Delete a user by ID

        Args:
            db (Session): The database session
            user_id (int): The ID of the user to delete

        Raises:
            UserNotFoundException: If the user with the given ID is not found
            DatabaseOperationException: If the database operation fails
        """
        existing_user = db.query(db_models.User).filter_by(id=user_id).first()
        if existing_user is None:
            raise UserNotFoundException(f"User with ID {user_id} not found!")

        try:
            db.delete(existing_user)
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                "delete_user", f"Integrity error: {str(e)}"
            )
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(
                "delete_user", f"Unexpected error: {str(e)}"
            )

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> user_schema.User:
        """
        Authenticate a user

        Args:
            db (Session): The database session
            email (str): The email of the user
            password (str): The password of the user

        Returns:
            user_schema.User: The authenticated user

        Raises:
            UserNotFoundException: If the user with the given email is not found
            ValueError: If the password is incorrect
        """
        user = UserService.get_user_by_email(db, email)
        if user is None:
            raise UserNotFoundException(f"User with email {email} not found")
        if not verify_password(password, user.hashed_password):
            raise ValueError("Incorrect password")
        return user
