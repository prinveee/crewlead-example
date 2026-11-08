"""Command line entry point: `tally data.csv`."""

from __future__ import annotations

import argparse
import csv
import json
import sys

from tally import __version__
from tally.stats import ColumnSummary, summarise


def _fmt(value: float | None) -> str:
    return "" if value is None else f"{value:g}"


def render_table(summaries: list[ColumnSummary]) -> str:
    header = ["column", "kind", "count", "min", "max", "mean", "distinct"]
    rows = [
        [
            s.name,
            s.kind,
            str(s.count),
            _fmt(s.minimum),
            _fmt(s.maximum),
            _fmt(s.mean),
            "" if s.distinct is None else str(s.distinct),
        ]
        for s in summaries
    ]
    widths = [max(len(r[i]) for r in [header, *rows]) for i in range(len(header))]
    lines = ["  ".join(cell.ljust(w) for cell, w in zip(r, widths)).rstrip() for r in [header, *rows]]
    return "\n".join(lines)


def render_json(summaries: list[ColumnSummary]) -> str:
    return json.dumps(
        [
            {
                "name": s.name,
                "kind": s.kind,
                "count": s.count,
                "min": s.minimum,
                "max": s.maximum,
                "mean": s.mean,
                "distinct": s.distinct,
            }
            for s in summaries
        ],
        indent=2,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tally", description="Summarise the columns of a CSV file.")
    parser.add_argument("path", help="CSV file with a header row")
    parser.add_argument("--version", action="version", version=f"tally {__version__}")
    parser.add_argument("--json", action="store_true", help="print the summaries as a JSON array")
    args = parser.parse_args(argv)

    try:
        with open(args.path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
            columns = list(reader.fieldnames or [])
    except OSError as exc:
        print(f"tally: {exc.strerror}: {args.path}", file=sys.stderr)
        return 2

    summaries = summarise(rows, columns)
    print(render_json(summaries) if args.json else render_table(summaries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
