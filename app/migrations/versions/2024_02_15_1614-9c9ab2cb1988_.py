"""empty message

Revision ID: 9c9ab2cb1988
Revises: 228afa5b00ed
Create Date: 2024-02-15 16:14:53.531426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c9ab2cb1988'
down_revision: Union[str, None] = '228afa5b00ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(), nullable=False),
    sa.Column('request_text', sa.String(), nullable=True),
    sa.Column('registration_date', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    # ### end Alembic commands ###
