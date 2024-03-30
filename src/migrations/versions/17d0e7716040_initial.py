"""initial

Revision ID: 17d0e7716040
Revises: bf11f0e7539f
Create Date: 2024-03-22 17:37:48.533812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17d0e7716040'
down_revision: Union[str, None] = 'bf11f0e7539f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
