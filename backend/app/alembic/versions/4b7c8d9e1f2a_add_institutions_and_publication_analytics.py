"""Add institutions and publication analytics

Revision ID: 4b7c8d9e1f2a
Revises: a7f4c2d1b9e8
Create Date: 2026-04-13 15:30:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4b7c8d9e1f2a"
down_revision = "a7f4c2d1b9e8"
branch_labels = None
depends_on = None


institution_type_enum = sa.Enum(
    'university',
    'college',
    'research_institute',
    name='institutiontype',
    create_type=False   # 🔥 THIS LINE FIXES EVERYTHING
)
institution_role_enum = sa.Enum(
    "admin",
    "faculty",
    "student",
    "researcher",
    "staff",
    name="institutionrole",
    create_type=False   # ✅ ADD THIS

)
publication_engagement_type_enum = sa.Enum(
    "view",
    "download",
    "save",
    "share",
    "citation",
    name="publicationengagementtype",
    create_type=False   # ✅ ADD THIS

)


def upgrade():
    bind = op.get_bind()

    op.create_table(
        "institution",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("domain", sa.String(length=255), nullable=True),
        sa.Column("institution_type", institution_type_enum, nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("onboarding_enabled", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_institution_slug"), "institution", ["slug"], unique=True)
    op.create_index(op.f("ix_institution_domain"), "institution", ["domain"], unique=True)

    op.create_table(
        "institutionmembership",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("institution_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("role", institution_role_enum, nullable=False),
        sa.Column("department", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["created_by_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["institution_id"], ["institution.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "institution_id",
            "user_id",
            name="uq_institution_membership_institution_user",
        ),
    )
    op.create_index(
        op.f("ix_institutionmembership_institution_id"),
        "institutionmembership",
        ["institution_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_institutionmembership_user_id"),
        "institutionmembership",
        ["user_id"],
        unique=False,
    )

    op.add_column("researcherinfo", sa.Column("user_id", sa.Uuid(), nullable=True))
    op.add_column("researcherinfo", sa.Column("department", sa.String(), nullable=True))
    op.add_column("researcherinfo", sa.Column("affiliation_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    op.create_index(op.f("ix_researcherinfo_user_id"), "researcherinfo", ["user_id"], unique=False)
    op.create_index(
        op.f("ix_researcherinfo_affiliation_verified"),
        "researcherinfo",
        ["affiliation_verified"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_researcherinfo_user_id_user",
        "researcherinfo",
        "user",
        ["user_id"],
        ["id"],
    )

    op.add_column("publication", sa.Column("citation_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("publication", sa.Column("download_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("publication", sa.Column("view_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("publication", sa.Column("save_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("publication", sa.Column("share_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("publication", sa.Column("last_engagement_at", sa.DateTime(timezone=True), nullable=True))

    op.create_table(
        "publicationanalyticsevent",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("publication_id", sa.Uuid(), nullable=False),
        sa.Column("actor_user_id", sa.Uuid(), nullable=True),
        sa.Column("event_type", publication_engagement_type_enum, nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["actor_user_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["publication_id"], ["publication.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_publicationanalyticsevent_publication_id"),
        "publicationanalyticsevent",
        ["publication_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_publicationanalyticsevent_event_type"),
        "publicationanalyticsevent",
        ["event_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_publicationanalyticsevent_occurred_at"),
        "publicationanalyticsevent",
        ["occurred_at"],
        unique=False,
    )

    op.alter_column("researcherinfo", "affiliation_verified", server_default=None)
    op.alter_column("publication", "citation_count", server_default=None)
    op.alter_column("publication", "download_count", server_default=None)
    op.alter_column("publication", "view_count", server_default=None)
    op.alter_column("publication", "save_count", server_default=None)
    op.alter_column("publication", "share_count", server_default=None)


def downgrade():
    op.drop_index(op.f("ix_publicationanalyticsevent_occurred_at"), table_name="publicationanalyticsevent")
    op.drop_index(op.f("ix_publicationanalyticsevent_event_type"), table_name="publicationanalyticsevent")
    op.drop_index(op.f("ix_publicationanalyticsevent_publication_id"), table_name="publicationanalyticsevent")
    op.drop_table("publicationanalyticsevent")

    op.drop_column("publication", "last_engagement_at")
    op.drop_column("publication", "share_count")
    op.drop_column("publication", "save_count")
    op.drop_column("publication", "view_count")
    op.drop_column("publication", "download_count")
    op.drop_column("publication", "citation_count")

    op.drop_constraint("fk_researcherinfo_user_id_user", "researcherinfo", type_="foreignkey")
    op.drop_index(op.f("ix_researcherinfo_affiliation_verified"), table_name="researcherinfo")
    op.drop_index(op.f("ix_researcherinfo_user_id"), table_name="researcherinfo")
    op.drop_column("researcherinfo", "affiliation_verified")
    op.drop_column("researcherinfo", "department")
    op.drop_column("researcherinfo", "user_id")

    op.drop_index(op.f("ix_institutionmembership_user_id"), table_name="institutionmembership")
    op.drop_index(op.f("ix_institutionmembership_institution_id"), table_name="institutionmembership")
    op.drop_table("institutionmembership")

    op.drop_index(op.f("ix_institution_domain"), table_name="institution")
    op.drop_index(op.f("ix_institution_slug"), table_name="institution")
    op.drop_table("institution")

    bind = op.get_bind()
    publication_engagement_type_enum.drop(bind, checkfirst=True)
    institution_role_enum.drop(bind, checkfirst=True)
    institution_type_enum.drop(bind, checkfirst=True)
