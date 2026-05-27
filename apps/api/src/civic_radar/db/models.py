"""SQLAlchemy ORM models for CivicRadar core entities."""

from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from civic_radar.db.session import Base


def _uuid() -> str:
    """Generate a UUID4 as string (portable across SQLite + Postgres)."""

    return str(uuid.uuid4())


class OpportunityStatus(enum.StrEnum):
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class ConfidenceLevel(enum.StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SourceType(enum.StrEnum):
    AGENCY = "agency"
    BOARD = "organizing_board"
    PORTAL = "portal"
    AGGREGATOR = "aggregator"


class EducationLevel(enum.StrEnum):
    FUNDAMENTAL = "fundamental"
    MEDIO = "medio"
    TECNICO = "tecnico"
    SUPERIOR = "superior"
    POS_GRADUACAO = "pos_graduacao"


class Source(Base):
    """A data source (organizing board, agency, portal or aggregator)."""

    __tablename__ = "source"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    source_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[SourceType] = mapped_column(
        Enum(SourceType, native_enum=False, length=32), nullable=False
    )
    base_url: Mapped[str] = mapped_column(String(512), nullable=False)
    quality_level: Mapped[ConfidenceLevel] = mapped_column(
        Enum(ConfidenceLevel, native_enum=False, length=16),
        default=ConfidenceLevel.MEDIUM,
        nullable=False,
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    parser_name: Mapped[str | None] = mapped_column(String(128))
    rate_limit_seconds: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    last_successful_check_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_error_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_error_message: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    opportunities: Mapped[list[Opportunity]] = relationship(
        back_populates="source", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Source {self.source_id!r}>"


class Opportunity(Base):
    """A public tender / position opening."""

    __tablename__ = "opportunity"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    source_pk: Mapped[str] = mapped_column(
        String(36), ForeignKey("source.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    organization: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    board: Mapped[str | None] = mapped_column(String(128), index=True)
    area: Mapped[str | None] = mapped_column(String(64), index=True)
    position_name: Mapped[str | None] = mapped_column(String(255))

    education_level: Mapped[EducationLevel | None] = mapped_column(
        Enum(EducationLevel, native_enum=False, length=32), index=True
    )

    salary_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    salary_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    vacancies: Mapped[int | None] = mapped_column(Integer)

    state: Mapped[str | None] = mapped_column(String(2), index=True)
    city: Mapped[str | None] = mapped_column(String(128))

    status: Mapped[OpportunityStatus] = mapped_column(
        Enum(OpportunityStatus, native_enum=False, length=16),
        default=OpportunityStatus.DRAFT,
        index=True,
        nullable=False,
    )

    registration_start_date: Mapped[date | None] = mapped_column(Date)
    registration_end_date: Mapped[date | None] = mapped_column(Date, index=True)
    exam_date: Mapped[date | None] = mapped_column(Date)

    source_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    original_url: Mapped[str | None] = mapped_column(String(1024))
    confidence_level: Mapped[ConfidenceLevel] = mapped_column(
        Enum(ConfidenceLevel, native_enum=False, length=16),
        default=ConfidenceLevel.MEDIUM,
        nullable=False,
    )

    keywords: Mapped[list[str] | None] = mapped_column(JSON)

    last_checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    source: Mapped[Source] = relationship(back_populates="opportunities")
    verifications: Mapped[list[OpportunityVerification]] = relationship(
        back_populates="opportunity", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_opportunity_status_state", "status", "state"),
        Index("idx_opportunity_area_status", "area", "status"),
        Index(
            "idx_opportunity_source_url_unique",
            "source_pk",
            "source_url",
            unique=True,
        ),
    )

    def __repr__(self) -> str:
        return f"<Opportunity {self.title!r} ({self.status})>"


class RawSnapshot(Base):
    """A raw snapshot of source content for reproducible re-parsing."""

    __tablename__ = "raw_snapshot"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    source_pk: Mapped[str] = mapped_column(
        String(36), ForeignKey("source.id", ondelete="CASCADE"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    content_type: Mapped[str] = mapped_column(String(64), nullable=False)
    raw_content_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    parser_version: Mapped[str | None] = mapped_column(String(32))
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<RawSnapshot {self.url!r} @ {self.captured_at}>"


class OpportunityVerification(Base):
    """Audit log of opportunity re-checks."""

    __tablename__ = "opportunity_verification"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    opportunity_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("opportunity.id", ondelete="CASCADE"), nullable=False
    )
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    check_result: Mapped[str] = mapped_column(String(32), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    opportunity: Mapped[Opportunity] = relationship(back_populates="verifications")
