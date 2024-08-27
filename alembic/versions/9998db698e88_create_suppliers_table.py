"""Create suppliers table

Revision ID: 9998db698e88
Revises: 
Create Date: 2024-08-27 17:02:47.905289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9998db698e88'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('suppliers', sa.Column('email', sa.String(), nullable=True))
    op.add_column('suppliers', sa.Column('phone', sa.String(), nullable=True))
    op.create_index(op.f('ix_suppliers_email'), 'suppliers', ['email'], unique=False)
    op.drop_column('suppliers', 'contact_info')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('suppliers', sa.Column('contact_info', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_suppliers_email'), table_name='suppliers')
    op.drop_column('suppliers', 'phone')
    op.drop_column('suppliers', 'email')
    # ### end Alembic commands ###
