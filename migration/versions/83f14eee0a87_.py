"""empty message

Revision ID: 83f14eee0a87
Revises: 91d11b4a6a7c
Create Date: 2019-12-02 17:24:57.414146

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.

revision = '83f14eee0a87'
down_revision = '91d11b4a6a7c'
branch_labels = None
depends_on = None



def upgrade():
    op.add_column('preference', sa.Column('distance', sa.Integer(), nullable=True))
    pass


def downgrade():
    pass
