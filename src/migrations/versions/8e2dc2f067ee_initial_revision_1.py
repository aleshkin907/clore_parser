"""initial revision 1

Revision ID: 8e2dc2f067ee
Revises: c618b00871e2
Create Date: 2024-03-22 18:04:14.163590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e2dc2f067ee'
down_revision: Union[str, None] = 'c618b00871e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
