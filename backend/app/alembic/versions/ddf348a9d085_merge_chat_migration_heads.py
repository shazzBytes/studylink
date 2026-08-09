"""merge chat migration heads

Revision ID: ddf348a9d085
Revises: 3acde1ae4f6e, d5a3e1c4b7f9
Create Date: 2026-08-10 02:01:06.434201

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'ddf348a9d085'
down_revision = ('3acde1ae4f6e', 'd5a3e1c4b7f9')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
