"""Changed user id datatype to UUID

Revision ID: 59b730a874fa
Revises: 82edb74b1f71
Create Date: 2024-08-29 17:09:09.957515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '59b730a874fa'
down_revision: Union[str, None] = '82edb74b1f71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    # Create a new UUID column
    op.add_column('users', sa.Column('new_id', postgresql.UUID(as_uuid=True), nullable=True))

    # Generate UUID for existing rows
    op.execute("UPDATE users SET new_id = uuid_generate_v4()")

    # Set the new column as not nullable
    op.alter_column('users', 'new_id', nullable=False)

    # Drop the old id column and rename the new one
    op.drop_column('users', 'id')
    op.alter_column('users', 'new_id', new_column_name='id')

    # Add primary key constraint to the new id column
    op.create_primary_key('pk_users', 'users', ['id'])

def downgrade():
    # Reverse the changes if needed
    op.execute("ALTER TABLE users DROP CONSTRAINT pk_users")
    op.alter_column('users', 'id', new_column_name='new_id')
    op.add_column('users', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.execute("UPDATE users SET id = DEFAULT")
    op.drop_column('users', 'new_id')
    op.create_primary_key('pk_users', 'users', ['id'])
