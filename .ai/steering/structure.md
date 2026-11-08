# Structure

<!-- Steering: always loaded into AGENTS.md. One page at most. Tell an agent
     where things live and which existing code to copy for a new one. -->

## Code map
| Where | What |
|---|---|
| `src/tally/stats.py` | Column statistics: `ColumnSummary`, `summarise_column`, `summarise`. Pure functions |
| `src/tally/cli.py` | Entry point `main(argv)`: argparse, reads the CSV, `render_table`, exit codes |
| `src/tally/__init__.py` | Package docstring and `__version__` |
| `tests/` | pytest tests, one file per module (`test_stats.py`, `test_cli.py`) |
| `examples/` | Sample CSV files (`orders.csv`) |
| `.github/workflows/` | CI (`ci.yml`) and the crewlead guard (`ai-guard.yml`) |

## Where new things go
| Adding a… | Put it in | Copy the pattern of |
|---|---|---|
| Statistic or column rule | `src/tally/stats.py` (+ a field on `ColumnSummary`) | `summarise_column`; test like `tests/test_stats.py::test_numeric_column_gets_min_max_mean` |
| Output column | `render_table` in `src/tally/cli.py` | the `header` / `rows` lists there |
| CLI flag or error case | `main()` in `src/tally/cli.py` | `--version`; the `OSError` branch; test like `tests/test_cli.py::test_missing_file_exits_2` |
| End-to-end check | `tests/test_cli.py` | `test_prints_a_table` (writes a CSV to `tmp_path`, reads `capsys`) |
| Sample data | `examples/` | `examples/orders.csv` |

## Conventions
- Naming: snake_case modules and functions; private helpers start with `_`
  (`_as_numbers`, `_fmt`). Every module starts with a one-line docstring and
  `from __future__ import annotations`. Type hints use `X | None`.
- Tests: plain pytest functions named `test_<behaviour>` (no classes), using
  `tmp_path` and `capsys` fixtures; CLI tests call `main([...])` directly
  instead of a subprocess.
- Commits: short imperative subject (`Initial tally CLI: per-column CSV summary`).

## Folder-specific rules
None proposed: the code is two modules; the rules above cover them.
