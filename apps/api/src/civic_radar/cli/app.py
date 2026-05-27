"""Typer CLI entry point."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Annotated

import typer
import uvicorn
from rich.console import Console
from rich.table import Table

from civic_radar import __version__
from civic_radar.cli.seed import run_seed
from civic_radar.config import get_settings
from civic_radar.db.session import create_engine_and_session

app = typer.Typer(
    name="civic_radar",
    help="🛰️  CivicRadar — open source radar for Brazilian public tenders",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)
console = Console()


@app.command()
def version() -> None:
    """Print the CivicRadar version."""

    console.print(f"[bold cyan]CivicRadar[/] v{__version__}")


@app.command()
def serve(
    host: Annotated[str, typer.Option(help="Host to bind")] = "0.0.0.0",
    port: Annotated[int, typer.Option(help="Port to bind")] = 8000,
    reload: Annotated[bool, typer.Option(help="Auto-reload on code changes")] = False,
    workers: Annotated[int, typer.Option(min=1, max=8)] = 1,
) -> None:
    """Start the FastAPI server with Uvicorn."""

    console.rule("[bold cyan]CivicRadar API")
    console.print(f"Starting on [bold]http://{host}:{port}[/]")
    console.print("Docs (Scalar): [bold]/docs[/]   ReDoc: [bold]/redoc[/]")
    console.rule()

    uvicorn.run(
        "civic_radar.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1,
        log_config=None,
        access_log=False,
    )


@app.command()
def seed(
    file: Annotated[
        Path,
        typer.Option(help="Seed JSON file path", exists=False),
    ] = Path("data/seeds/opportunities_seed.json"),
    reset: Annotated[bool, typer.Option(help="Drop and recreate all rows before seeding")] = False,
) -> None:
    """Populate the database with seed data."""

    settings = get_settings()
    asyncio.run(run_seed(settings, seed_path=file, reset=reset, console=console))


@app.command()
def stats() -> None:
    """Print database stats to the terminal."""

    settings = get_settings()
    asyncio.run(_print_stats(settings))


async def _print_stats(settings) -> None:  # type: ignore[no-untyped-def]
    from sqlalchemy import func, select

    from civic_radar.db.models import Opportunity, OpportunityStatus, Source

    _, factory = create_engine_and_session(settings)
    async with factory() as session:
        total = (await session.execute(select(func.count()).select_from(Opportunity))).scalar_one()
        open_count = (
            await session.execute(
                select(func.count())
                .select_from(Opportunity)
                .where(Opportunity.status == OpportunityStatus.OPEN)
            )
        ).scalar_one()
        sources = (await session.execute(select(func.count()).select_from(Source))).scalar_one()

    table = Table(title="CivicRadar — stats", show_header=False, box=None)
    table.add_row("[bold]Total opportunities[/]", str(total))
    table.add_row("[bold green]Open[/]", str(open_count))
    table.add_row("[bold]Sources[/]", str(sources))
    console.print(table)


@app.command(name="parse-fixture")
def parse_fixture(
    source: Annotated[str, typer.Option(help="Source ID (e.g. cebraspe)")],
    fixture: Annotated[Path, typer.Argument(help="HTML or PDF fixture path", exists=True)],
) -> None:
    """Run a parser against a fixture file. Useful for offline development.

    Example:
        civic_radar parse-fixture --source cebraspe path/to/fixture.html
    """

    try:
        from crawlers.core.models import RawSnapshot
        from crawlers.core.registry import SourceRegistry
    except ImportError as exc:
        console.print(f"[red]crawlers package not available: {exc}[/]")
        raise typer.Exit(code=1) from exc

    registry = SourceRegistry()
    parser = registry.get_parser(source)
    if parser is None:
        console.print(f"[red]No parser registered for source '{source}'[/]")
        console.print(f"Available: {registry.list_ids()}")
        raise typer.Exit(code=2)

    import hashlib

    content = fixture.read_bytes()
    snapshot = RawSnapshot(
        source_id=source,
        url=f"file://{fixture.resolve()}",
        content=content,
        content_type="text/html" if fixture.suffix in {".html", ".htm"} else "application/pdf",
        content_hash=hashlib.sha256(content).hexdigest(),
    )

    parsed = parser.parse(snapshot)
    console.rule(f"[bold]{source}[/] · parser v{parser.parser_version}")
    console.print(f"[green]Extracted[/] {len(parsed)} opportunity(ies)")
    for opp in parsed:
        console.print(f"  • [bold]{opp.title}[/] — {opp.organization} ({opp.state or '?'})")


@app.command(name="export")
def export_data(
    output_format: Annotated[
        str, typer.Option("--format", "-f", help="Output format: json|csv")
    ] = "json",
    output: Annotated[Path | None, typer.Option(help="Output file (default: stdout)")] = None,
) -> None:
    """Export opportunities to JSON or CSV."""

    if output_format not in {"json", "csv"}:
        console.print(f"[red]Invalid format '{output_format}'. Use 'json' or 'csv'.[/]")
        raise typer.Exit(code=2)

    settings = get_settings()
    asyncio.run(_run_export(settings, output_format=output_format, output=output))


async def _run_export(settings, *, output_format: str, output: Path | None) -> None:  # type: ignore[no-untyped-def]
    from sqlalchemy import select

    from civic_radar.db.models import Opportunity
    from civic_radar.schemas.opportunity import OpportunityRead

    _, factory = create_engine_and_session(settings)
    async with factory() as session:
        rows = (await session.execute(select(Opportunity))).scalars().all()

    payload = [OpportunityRead.model_validate(row).model_dump(mode="json") for row in rows]

    if output_format == "json":
        data = json.dumps(payload, ensure_ascii=False, indent=2, default=str)
    else:
        import csv
        import io

        buf = io.StringIO()
        if payload:
            writer = csv.DictWriter(buf, fieldnames=list(payload[0].keys()))
            writer.writeheader()
            writer.writerows(payload)
        data = buf.getvalue()

    if output:
        output.write_text(data, encoding="utf-8")
        console.print(f"[green]Wrote[/] {len(payload)} rows to [bold]{output}[/]")
    else:
        sys.stdout.write(data)
