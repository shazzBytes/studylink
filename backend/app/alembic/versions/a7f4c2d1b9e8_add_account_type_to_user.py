"""add account_type to user

Revision ID: a7f4c2d1b9e8
Revises: f1b9c3e4a7d2
Create Date: 2026-04-11 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "a7f4c2d1b9e8"
down_revision = "f1b9c3e4a7d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column(
            "account_type",
            sa.String(length=32),
            nullable=False,
            server_default="student",
        ),
    )


def downgrade() -> None:
    op.drop_column("user", "account_type")
