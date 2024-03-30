"""initial revision 1

Revision ID: 4858a09ab05e
Revises: 8e2dc2f067ee
Create Date: 2024-03-22 18:06:47.520817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4858a09ab05e'
down_revision: Union[str, None] = '8e2dc2f067ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
