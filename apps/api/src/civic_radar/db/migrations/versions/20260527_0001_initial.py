"""Initial schema — source, opportunity, raw_snapshot, opportunity_verification

Revision ID: 20260527_0001
Revises:
Create Date: 2026-05-27 00:00:00

"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260527_0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "source",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("source_id", sa.String(64), unique=True, nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("type", sa.String(32), nullable=False),
        sa.Column("base_url", sa.String(512), nullable=False),
        sa.Column("quality_level", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("parser_name", sa.String(128)),
        sa.Column("rate_limit_seconds", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("last_successful_check_at", sa.DateTime(timezone=True)),
        sa.Column("last_error_at", sa.DateTime(timezone=True)),
        sa.Column("last_error_message", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "opportunity",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("source_pk", sa.String(36), sa.ForeignKey("source.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("organization", sa.String(255), nullable=False, index=True),
        sa.Column("board", sa.String(128), index=True),
        sa.Column("area", sa.String(64), index=True),
        sa.Column("position_name", sa.String(255)),
        sa.Column("education_level", sa.String(32), index=True),
        sa.Column("salary_min", sa.Numeric(12, 2)),
        sa.Column("salary_max", sa.Numeric(12, 2)),
        sa.Column("vacancies", sa.Integer()),
        sa.Column("state", sa.String(2), index=True),
        sa.Column("city", sa.String(128)),
        sa.Column("status", sa.String(16), nullable=False, server_default="draft", index=True),
        sa.Column("registration_start_date", sa.Date()),
        sa.Column("registration_end_date", sa.Date(), index=True),
        sa.Column("exam_date", sa.Date()),
        sa.Column("source_url", sa.String(1024), nullable=False),
        sa.Column("original_url", sa.String(1024)),
        sa.Column("confidence_level", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("keywords", sa.JSON()),
        sa.Column("last_checked_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_index(
        "idx_opportunity_status_state", "opportunity", ["status", "state"]
    )
    op.create_index(
        "idx_opportunity_area_status", "opportunity", ["area", "status"]
    )
    op.create_index(
        "idx_opportunity_source_url_unique",
        "opportunity",
        ["source_pk", "source_url"],
        unique=True,
    )

    op.create_table(
        "raw_snapshot",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("source_pk", sa.String(36), sa.ForeignKey("source.id", ondelete="CASCADE"), nullable=False),
        sa.Column("url", sa.String(1024), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False, index=True),
        sa.Column("content_type", sa.String(64), nullable=False),
        sa.Column("raw_content_path", sa.String(1024), nullable=False),
        sa.Column("parser_version", sa.String(32)),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "opportunity_verification",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("opportunity_id", sa.String(36), sa.ForeignKey("opportunity.id", ondelete="CASCADE"), nullable=False),
        sa.Column("checked_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("check_result", sa.String(32), nullable=False),
        sa.Column("notes", sa.Text()),
    )


def downgrade() -> None:
    op.drop_table("opportunity_verification")
    op.drop_table("raw_snapshot")
    op.drop_index("idx_opportunity_source_url_unique", table_name="opportunity")
    op.drop_index("idx_opportunity_area_status", table_name="opportunity")
    op.drop_index("idx_opportunity_status_state", table_name="opportunity")
    op.drop_table("opportunity")
    op.drop_table("source")
