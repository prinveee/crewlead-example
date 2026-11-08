# tally

A tiny CLI that summarises the columns of a CSV file: for number columns the
min, max and mean; for text columns the number of distinct values.

```console
$ tally examples/orders.csv
```

## Develop

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
ruff check . && pytest -q
```

## About this repository

This is an **example project for [crewlead](https://github.com/prinveee/crewlead)**.
Its issues, plan comments, draft pull requests and reviews were written by AI
agents running the crewlead flow for real (intake → planner → `/go` →
implementor → reviewer → a person merges). Browse the closed and open issues
and pull requests to see each stage.
