"""Column statistics. Pure functions: no I/O here."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ColumnSummary:
    name: str
    count: int
    kind: str  # "number" or "text"
    minimum: float | None = None
    maximum: float | None = None
    mean: float | None = None
    distinct: int | None = None


def _as_numbers(values: list[str]) -> list[float] | None:
    """Return the values as floats, or None if any of them is not a number."""
    numbers = []
    for value in values:
        try:
            numbers.append(float(value))
        except ValueError:
            return None
    return numbers


def summarise_column(name: str, values: list[str]) -> ColumnSummary:
    numbers = _as_numbers(values)
    if numbers:
        return ColumnSummary(
            name=name,
            count=len(values),
            kind="number",
            minimum=min(numbers),
            maximum=max(numbers),
            mean=sum(numbers) / len(numbers),
        )
    return ColumnSummary(name=name, count=len(values), kind="text", distinct=len(set(values)))


def summarise(rows: list[dict[str, str]], columns: list[str]) -> list[ColumnSummary]:
    return [summarise_column(c, [row.get(c) or "" for row in rows]) for c in columns]
