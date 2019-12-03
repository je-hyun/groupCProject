"""empty message

Revision ID: 91d11b4a6a7c
Revises: fea2a4a7ef4d
Create Date: 2019-12-02 15:48:50.326318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91d11b4a6a7c'
down_revision = 'fea2a4a7ef4d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('preference', sa.Column('user_id', sa.Integer(), nullable=True))
    pass


def downgrade():
    pass
