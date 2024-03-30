"""initial revision 1

Revision ID: ad6975278460
Revises: 8ad61af81d14
Create Date: 2024-03-22 18:01:08.600263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad6975278460'
down_revision: Union[str, None] = '8ad61af81d14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
