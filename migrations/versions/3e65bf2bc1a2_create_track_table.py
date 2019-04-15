"""create track table

Revision ID: 3e65bf2bc1a2
Revises: 
Create Date: 2019-01-03 18:19:30.706943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e65bf2bc1a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tracks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('stream_url', sa.String(), nullable=False),
        sa.Column('title', sa.String()),
        sa.Column('artist', sa.String()),
        sa.Column('page_url', sa.String()),
    )


def downgrade():
    op.drop_table('tracks')
