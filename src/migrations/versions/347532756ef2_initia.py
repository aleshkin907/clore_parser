"""initia

Revision ID: 347532756ef2
Revises: 669dcd3fb1b0
Create Date: 2024-03-22 17:40:38.008011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '347532756ef2'
down_revision: Union[str, None] = '669dcd3fb1b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
