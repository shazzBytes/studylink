"""Add chat and message tables

Revision ID: b4c6a1d2e3f4
Revises: 870d2ef8b63a
Create Date: 2026-02-26 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b4c6a1d2e3f4"
down_revision = "870d2ef8b63a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chat",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("participants", sa.JSON(), nullable=False),
        sa.Column("last_message", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_chat_user_id"), "chat", ["user_id"], unique=False)
    op.create_index(
        op.f("ix_chat_is_deleted"), "chat", ["is_deleted"], unique=False
    )

    op.create_table(
        "message",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("chat_id", sa.Uuid(), nullable=False),
        sa.Column("sender_id", sa.Uuid(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("attachments", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["chat_id"], ["chat.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sender_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_message_chat_id"), "message", ["chat_id"], unique=False)
    op.create_index(
        op.f("ix_message_sender_id"), "message", ["sender_id"], unique=False
    )
    op.create_index(
        op.f("ix_message_is_deleted"), "message", ["is_deleted"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_message_is_deleted"), table_name="message")
    op.drop_index(op.f("ix_message_sender_id"), table_name="message")
    op.drop_index(op.f("ix_message_chat_id"), table_name="message")
    op.drop_table("message")

    op.drop_index(op.f("ix_chat_is_deleted"), table_name="chat")
    op.drop_index(op.f("ix_chat_user_id"), table_name="chat")
    op.drop_table("chat")
