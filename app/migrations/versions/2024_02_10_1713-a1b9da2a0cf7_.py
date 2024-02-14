"""empty message

Revision ID: a1b9da2a0cf7
Revises: 493783b7caaf
Create Date: 2024-02-10 17:13:55.833259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b9da2a0cf7'
down_revision: Union[str, None] = '493783b7caaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    None


def downgrade() -> None:
    None
