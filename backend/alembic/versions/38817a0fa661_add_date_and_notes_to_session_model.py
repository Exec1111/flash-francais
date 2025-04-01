"""Add date and notes to Session model

Revision ID: 38817a0fa661
Revises: ea831a4299c8
Create Date: 2025-04-01 21:11:18.955972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38817a0fa661'
down_revision: Union[str, None] = 'ea831a4299c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sessions', sa.Column('date', sa.DateTime(), nullable=False))
    op.add_column('sessions', sa.Column('notes', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sessions', 'notes')
    op.drop_column('sessions', 'date')
    # ### end Alembic commands ###
