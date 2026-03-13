"""Add chat type column

Revision ID: d5a3e1c4b7f9
Revises: c2f4a9b8d1e2
Create Date: 2026-03-10 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d5a3e1c4b7f9"
down_revision = "c2f4a9b8d1e2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "chat",
        sa.Column("chat_type", sa.String(length=16), nullable=True, server_default="dm"),
    )
    op.execute(
        """
        UPDATE chat
        SET chat_type = CASE
            WHEN json_array_length(participants) > 2 THEN 'group'
            ELSE 'dm'
        END
        """
    )
    op.alter_column("chat", "chat_type", nullable=False, server_default=None)
    op.create_index(op.f("ix_chat_chat_type"), "chat", ["chat_type"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_chat_chat_type"), table_name="chat")
    op.drop_column("chat", "chat_type")
