"""initial revision

Revision ID: 8ad61af81d14
Revises: 347532756ef2
Create Date: 2024-03-22 17:46:10.219516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ad61af81d14'
down_revision: Union[str, None] = '347532756ef2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
