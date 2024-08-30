from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import db_models
from app.exceptions.database import DatabaseOperationException
from app.exceptions.supplier import (
    SupplierAlreadyExistsException,
    SupplierNotFoundException,
)
from app.schemas import supplier as supplier_schema


class SupplierService:
    @staticmethod
    def get_supplier(db: Session, supplier_id: UUID) -> supplier_schema.Supplier:
        """
        Get a supplier by ID

        Args:
            db (Session): The database session
            supplier_id (UUID): The ID of the supplier to retrieve

        Returns:
            supplier_schema.Supplier: The supplier with the given ID

        Raises:
            SupplierNotFoundException: If the supplier with the given ID is not found
        """
        supplier = db.query(db_models.Supplier).filter_by(id=supplier_id).first()
        if supplier is None:
            raise SupplierNotFoundException(supplier_id)
        return supplier

    @staticmethod
    def get_suppliers(
        db: Session, skip: int = 0, limit: int = 100
    ) -> list[supplier_schema.Supplier]:
        """
        Get all the list of suppliers

        Args:
            db (Session): The database session

        Returns:
            list[supplier_schema.Supplier]: A list of all suppliers
        """
        suppliers = db.query(db_models.Supplier).offset(skip).limit(limit).all()
        return suppliers

    @staticmethod
    def create_supplier(
        db: Session, supplier: supplier_schema.SupplierCreate
    ) -> supplier_schema.Supplier:
        """
        Create a new supplier

        Args:
            db (Session): The database session
            supplier (supplier_schema.SupplierCreate): The suppliers data to store/create

        Returns:
            supplier_schema.Supplier: The newly created supplier

        Raises:
            SupplierAlreadyExistsException: If a supplier with the same email already exists
            DatabaseOperationException: If the database operation fails
        """
        # Check if supplier already exists
        existing_supplier = (
            db.query(db_models.Supplier)
            .filter(
                (db_models.Supplier.email == supplier.email)
                | (db_models.Supplier.phone == supplier.phone)
            )
            .first()
        )
        if existing_supplier:
            if existing_supplier.email == supplier.email:
                raise SupplierAlreadyExistsException("email", supplier.email)
            else:
                raise SupplierAlreadyExistsException("phone", supplier.phone)

        # If not, create the new supplier
        new_supplier = db_models.Supplier(**supplier.dict())
        try:
            db.add(new_supplier)
            db.commit()
            db.refresh(new_supplier)
            return new_supplier
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                "create_supplier", f"Integrity error: {str(e)}"
            )
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(
                "create_supplier", f"Unexpected error: {str(e)}"
            )

    @staticmethod
    def update_supplier(
        db: Session, supplier_id: UUID, supplier: supplier_schema.SupplierUpdate
    ) -> supplier_schema.Supplier:
        """
        Update a supplier by ID

        Args:
            db (Session): The database session
            supplier_id (UUID): The ID of the supplier to update
            supplier (supplier_schema.SupplierUpdate): The updated supplier data

        Returns:
            supplier_schema.Supplier: The updated supplier

        Raises:
            SupplierNotFoundException: If the supplier with the given ID is not found
            DatabaseOperationException: If the database operation fails
        """
        existing_supplier = (
            db.query(db_models.Supplier).filter_by(id=supplier_id).first()
        )
        if existing_supplier is None:
            raise SupplierNotFoundException(
                f"Supplier with ID {supplier_id} not found!"
            )

        # Update the supplier data if exists
        update_data = {k: v for k, v in supplier.dict().items() if v is not None}
        for key, value in update_data.items():
            setattr(
                existing_supplier, key, value
            )  # This automatically updates the supplier data with new values

        try:
            db.commit()
            db.refresh(existing_supplier)
            return existing_supplier
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                "update_supplier", f"Integrity error: {str(e)}"
            )
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(
                "update_supplier", f"Unexpected error: {str(e)}"
            )

    @staticmethod
    def delete_supplier(db: Session, supplier_id: UUID) -> None:
        """
        Delete a supplier by ID

        Args:
            db (Session): The database session
            supplier_id (UUID): The ID of the supplier to delete

        Raises:
            SupplierNotFoundException: If the supplier with the given ID is not found
            DatabaseOperationException: If the database operation fails
        """
        existing_supplier = (
            db.query(db_models.Supplier).filter_by(id=supplier_id).first()
        )
        if existing_supplier is None:
            raise SupplierNotFoundException(
                f"Supplier with ID {supplier_id} not found!"
            )

        try:
            db.delete(existing_supplier)
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise DatabaseOperationException(
                "delete_supplier", f"Integrity error: {str(e)}"
            )
        except Exception as e:
            db.rollback()
            raise DatabaseOperationException(
                "delete_supplier", f"Unexpected error: {str(e)}"
            )
