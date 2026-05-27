"""Database seeding helpers."""

from __future__ import annotations

import json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from rich.console import Console
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from civic_radar.config import Settings
from civic_radar.db.models import (
    ConfidenceLevel,
    EducationLevel,
    Opportunity,
    OpportunityStatus,
    Source,
    SourceType,
)
from civic_radar.db.session import Base, create_engine_and_session

DEFAULT_SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "cebraspe",
        "name": "Cebraspe",
        "type": SourceType.BOARD,
        "base_url": "https://www.cebraspe.org.br/concursos/",
        "quality_level": ConfidenceLevel.HIGH,
        "parser_name": "cebraspe_v1",
        "rate_limit_seconds": 10,
    },
    {
        "source_id": "fgv",
        "name": "FGV CONHECIMENTO",
        "type": SourceType.BOARD,
        "base_url": "https://conhecimento.fgv.br/concursos",
        "quality_level": ConfidenceLevel.HIGH,
        "parser_name": "fgv_v1",
        "rate_limit_seconds": 10,
    },
    {
        "source_id": "pci-concursos",
        "name": "PCI Concursos",
        "type": SourceType.AGGREGATOR,
        "base_url": "https://www.pciconcursos.com.br/",
        "quality_level": ConfidenceLevel.MEDIUM,
        "parser_name": "pci_concursos_v1",
        "rate_limit_seconds": 15,
    },
]


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _coerce_opportunity(raw: dict[str, Any], source_map: dict[str, str]) -> dict[str, Any]:
    source_id = raw["source_id"]
    if source_id not in source_map:
        raise ValueError(f"Unknown source_id in seed: {source_id}")
    return {
        "source_pk": source_map[source_id],
        "title": raw["title"],
        "description": raw.get("description"),
        "organization": raw["organization"],
        "board": raw.get("board"),
        "area": raw.get("area"),
        "position_name": raw.get("position_name"),
        "education_level": (
            EducationLevel(raw["education_level"]) if raw.get("education_level") else None
        ),
        "salary_min": Decimal(str(raw["salary_min"])) if raw.get("salary_min") else None,
        "salary_max": Decimal(str(raw["salary_max"])) if raw.get("salary_max") else None,
        "vacancies": raw.get("vacancies"),
        "state": raw.get("state"),
        "city": raw.get("city"),
        "status": OpportunityStatus(raw.get("status", "open")),
        "registration_start_date": _parse_date(raw.get("registration_start_date")),
        "registration_end_date": _parse_date(raw.get("registration_end_date")),
        "exam_date": _parse_date(raw.get("exam_date")),
        "source_url": raw["source_url"],
        "original_url": raw.get("original_url"),
        "confidence_level": ConfidenceLevel(raw.get("confidence_level", "high")),
        "keywords": raw.get("keywords"),
    }


async def run_seed(
    settings: Settings,
    *,
    seed_path: Path,
    reset: bool = False,
    console: Console | None = None,
) -> None:
    """Run database seeding from a JSON file."""

    console = console or Console()
    engine, factory = create_engine_and_session(settings)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with factory() as session:
        await _seed_sources(session, console=console, reset=reset)
        source_map = await _source_map(session)
        await _seed_opportunities(
            session, source_map, seed_path=seed_path, console=console, reset=reset
        )
        await session.commit()


async def _seed_sources(session: AsyncSession, *, console: Console, reset: bool) -> None:
    if reset:
        await session.execute(delete(Source))

    existing_ids = {row[0] for row in (await session.execute(select(Source.source_id))).all()}

    added = 0
    for src in DEFAULT_SOURCES:
        if src["source_id"] in existing_ids:
            continue
        session.add(Source(**src))
        added += 1

    await session.flush()
    console.print(f"[green]Seeded[/] {added} sources ({len(DEFAULT_SOURCES) - added} existed)")


async def _source_map(session: AsyncSession) -> dict[str, str]:
    rows = (await session.execute(select(Source.source_id, Source.id))).all()
    return {row.source_id: row.id for row in rows}


async def _seed_opportunities(
    session: AsyncSession,
    source_map: dict[str, str],
    *,
    seed_path: Path,
    console: Console,
    reset: bool,
) -> None:
    if not seed_path.exists():
        console.print(f"[yellow]No seed file at {seed_path}[/] — skipping opportunities")
        return

    if reset:
        await session.execute(delete(Opportunity))

    raws: list[dict[str, Any]] = json.loads(seed_path.read_text(encoding="utf-8"))
    added = 0
    for raw in raws:
        try:
            data = _coerce_opportunity(raw, source_map)
        except (KeyError, ValueError) as exc:
            console.print(f"[red]Skip invalid seed row: {exc}[/]")
            continue
        session.add(Opportunity(**data))
        added += 1

    await session.flush()
    console.print(f"[green]Seeded[/] {added} opportunities from {seed_path}")
