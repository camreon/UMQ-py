"""add playlist table

Revision ID: 62f9339e4800
Revises: 3e65bf2bc1a2
Create Date: 2020-07-16 21:21:17.036271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62f9339e4800'
down_revision = '3e65bf2bc1a2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'playlists',
        sa.Column('id', sa.Integer(), primary_key=True),
    )

    op.add_column('tracks', sa.Column('playlist_id', sa.Integer()))

    op.create_foreign_key(None, 'tracks', 'playlists', ['playlist_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'tracks', type_='foreignkey')
    op.drop_column('tracks', 'playlist_id')
    op.drop_table('playlists')
