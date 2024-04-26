"""refactor pwd type

Revision ID: 033109de0c76
Revises: bdbf436795d9
Create Date: 2024-04-26 01:03:48.084611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '033109de0c76'
down_revision: Union[str, None] = 'bdbf436795d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('users', 'hashed_password',
    #            existing_type=sa.VARCHAR(),
    #            type_=sa.LargeBinary(),
    #            using="hashed_password::bytea",
    #            schema='public',
    #            existing_nullable=False)
    op.execute('ALTER TABLE public.users ALTER COLUMN hashed_password TYPE BYTEA USING hashed_password::bytea')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###
