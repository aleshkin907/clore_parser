"""initial 1

Revision ID: 669dcd3fb1b0
Revises: 17d0e7716040
Create Date: 2024-03-22 17:37:56.297888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '669dcd3fb1b0'
down_revision: Union[str, None] = '17d0e7716040'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
