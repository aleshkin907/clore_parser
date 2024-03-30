"""initial revision 1

Revision ID: c618b00871e2
Revises: ad6975278460
Create Date: 2024-03-22 18:02:53.781354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c618b00871e2'
down_revision: Union[str, None] = 'ad6975278460'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
