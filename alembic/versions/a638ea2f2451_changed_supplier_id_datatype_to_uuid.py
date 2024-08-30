"""Changed supplier id datatype to UUID

Revision ID: a638ea2f2451
Revises: 59b730a874fa
Create Date: 2024-08-30 07:04:50.926784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a638ea2f2451'
down_revision: Union[str, None] = '59b730a874fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create a new UUID column
    op.add_column('suppliers', sa.Column('new_id', postgresql.UUID(as_uuid=True), nullable=True))

    # Generate a UUID for each existing row
    op.execute("UPDATE suppliers SET new_id = uuid_generate_v4()")

    # Set the new column as not nullable
    op.alter_column('suppliers', 'new_id', nullable=False)

    # Drop the old primary key constraint
    op.drop_constraint('suppliers_pkey', 'suppliers', type_='primary')

    # Drop the old id column
    op.drop_column('suppliers', 'id')

    # Rename the new_id column to id
    op.alter_column('suppliers', 'new_id', new_column_name='id')

    # Add the primary key constraint to the new id column
    op.create_primary_key('suppliers_pkey', 'suppliers', ['id'])

def downgrade():
    # Create a new integer id column
    op.add_column('suppliers', sa.Column('new_id', sa.Integer(), autoincrement=True, nullable=True))

    # Generate sequential IDs
    op.execute("UPDATE suppliers SET new_id = nextval('suppliers_id_seq'::regclass)")

    # Set the new column as not nullable
    op.alter_column('suppliers', 'new_id', nullable=False)

    # Drop the old primary key constraint
    op.drop_constraint('suppliers_pkey', 'suppliers', type_='primary')

    # Drop the UUID id column
    op.drop_column('suppliers', 'id')

    # Rename the new_id column to id
    op.alter_column('suppliers', 'new_id', new_column_name='id')

    # Add the primary key constraint to the new id column
    op.create_primary_key('suppliers_pkey', 'suppliers', ['id'])
