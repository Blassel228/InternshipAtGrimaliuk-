"""empty message

Revision ID: 76f3a4912d1d
Revises: b836791753be
Create Date: 2024-02-16 22:34:30.994107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76f3a4912d1d'
down_revision: Union[str, None] = '776b083252d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('company',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('registration_date', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('visible', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name='company_owner_id_fkey', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='company_pkey'),
    sa.UniqueConstraint('name', name='company_name_key'))


def downgrade() -> None:
    op.drop_table('company')