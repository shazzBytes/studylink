"""Add project tables and merge heads

Revision ID: f1b9c3e4a7d2
Revises: 3acde1ae4f6e, d5a3e1c4b7f9
Create Date: 2026-04-05 16:05:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f1b9c3e4a7d2"
down_revision = ("3acde1ae4f6e", "d5a3e1c4b7f9")
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "project",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("domain", sa.String(length=255), nullable=False),
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_domain"), "project", ["domain"], unique=True)
    op.create_index(op.f("ix_project_is_deleted"), "project", ["is_deleted"], unique=False)
    op.create_index(op.f("ix_project_owner_id"), "project", ["owner_id"], unique=False)

    op.create_table(
        "projectmember",
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("added_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("project_id", "user_id"),
    )
    op.create_index(op.f("ix_projectmember_project_id"), "projectmember", ["project_id"], unique=False)
    op.create_index(op.f("ix_projectmember_role"), "projectmember", ["role"], unique=False)
    op.create_index(op.f("ix_projectmember_user_id"), "projectmember", ["user_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_projectmember_user_id"), table_name="projectmember")
    op.drop_index(op.f("ix_projectmember_role"), table_name="projectmember")
    op.drop_index(op.f("ix_projectmember_project_id"), table_name="projectmember")
    op.drop_table("projectmember")

    op.drop_index(op.f("ix_project_owner_id"), table_name="project")
    op.drop_index(op.f("ix_project_is_deleted"), table_name="project")
    op.drop_index(op.f("ix_project_domain"), table_name="project")
    op.drop_table("project")
