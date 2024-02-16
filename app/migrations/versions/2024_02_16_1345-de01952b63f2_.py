"""empty message

Revision ID: de01952b63f2
Revises: 9c9ab2cb1988
Create Date: 2024-02-16 13:45:22.900536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de01952b63f2'
down_revision: Union[str, None] = '9c9ab2cb1988'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    None

def downgrade() -> None:
    None
