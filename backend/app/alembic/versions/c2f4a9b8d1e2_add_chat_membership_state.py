"""Add chat membership state columns

Revision ID: c2f4a9b8d1e2
Revises: b4c6a1d2e3f4
Create Date: 2026-03-10 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c2f4a9b8d1e2"
down_revision = "b4c6a1d2e3f4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("chat", sa.Column("member_states", sa.JSON(), nullable=True))
    op.add_column("chat", sa.Column("reported_by", sa.JSON(), nullable=True))

    op.execute("UPDATE chat SET member_states = '{}'::json")
    op.execute("UPDATE chat SET reported_by = '[]'::json")

    op.alter_column("chat", "member_states", nullable=False)
    op.alter_column("chat", "reported_by", nullable=False)


def downgrade():
    op.drop_column("chat", "reported_by")
    op.drop_column("chat", "member_states")
