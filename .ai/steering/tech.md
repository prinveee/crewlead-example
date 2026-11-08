# Tech

<!-- Steering: always loaded into AGENTS.md. One page at most. Summarise the
     architecture decisions agents must respect; link the full ADRs. -->

## Stack
| Layer | Choice |
|---|---|
| Language | Python `>=3.11` (`pyproject.toml`); CI tests 3.11, 3.12, 3.13 |
| Runtime libraries | Standard library only (`argparse`, `csv`, `dataclasses`) |
| Packaging | hatchling, `src/` layout; console script `tally = "tally.cli:main"` |
| Lint | ruff `>=0.6`, `line-length = 100` (`[tool.ruff]`) |
| Tests | pytest `>=8`, `testpaths = ["tests"]` |
| CI | GitHub Actions `.github/workflows/ci.yml` (ruff + pytest) and `ai-guard.yml` |

## Decisions agents must respect
1. `src/tally/stats.py` is pure: no I/O, no printing (its module docstring).
   File reading, argument parsing and output belong in `src/tally/cli.py`.
2. No runtime dependencies: `dependencies = []` in `pyproject.toml`
   `[assumption: deliberate]`. Adding one is a stop (AGENTS.md §7).
3. Errors the user can cause (missing file) print `tally: <reason>: <path>` to
   stderr and return exit code 2 (`cli.py`, `tests/test_cli.py::test_missing_file_exits_2`).

## Commands
Exact commands live in `.ai/project.yml` → `commands`. Agents run only
`commands.test_local` on a developer machine; CI runs `commands.test_full`.

## Local machine
- Use the project venv: `. .venv/bin/activate` (`pip install -e ".[dev]"` once).
- No databases, services or credentials. The suite is tiny (5 tests, < 1 s),
  so `test_local` runs all of it.

## Deploy
Nothing is deployed or published: no release workflow exists. Agents never
publish to PyPI or tag releases.

## Deeper docs
- `README.md` → *Develop*.
