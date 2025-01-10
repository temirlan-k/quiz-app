"""fill db with fake data

Revision ID: 23c7fcb16ff4
Revises: c6d24a26e7fb
Create Date: 2025-01-10 16:54:53.766061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23c7fcb16ff4'
down_revision: Union[str, None] = 'c6d24a26e7fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    with open('migrations/init.sql', 'r') as file:
        connection.execute(file.read())
    pass


def downgrade() -> None:
    pass
