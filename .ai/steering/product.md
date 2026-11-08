# Product

<!-- Steering: always loaded into AGENTS.md. One page at most. This is a
     SUMMARY: when the project has deeper docs (BMAD PRD, project-context),
     link them and let them win on any disagreement — then fix this file. -->

## What and for whom
`tally` is a tiny command-line tool: `tally data.csv` prints one row per column
of a CSV file. For a number column it shows min, max and mean; for a text column,
the number of distinct values (README). It saves the user from opening a
spreadsheet just to get a feel for a file. The repository is also the public
example project for crewlead: its issues and PRs show the flow at work.

## Users
| User | Needs | Context (device, skill, language) |
|---|---|---|
| Someone with a CSV at hand `[assumption]` | A quick per-column overview in the terminal | Terminal, comfortable with a CLI, English output |
| Readers of the crewlead example | Real issues, plans and PRs to learn the flow from | GitHub web UI |

## Scope
- **In:** per-column summaries of one CSV file with a header row, printed as a
  plain-text table.
- **Out (non-goals):** `[assumption]` charts, other file formats, editing or
  writing data, runtime dependencies.

## Business rules that must always hold
Full list, with sources and known gaps: `.ai/business-rules.md`.
- **BR-STATS-01** A number column is summarised with min, max and mean.
- **BR-STATS-02** A text column is summarised with its number of distinct values.
- **BR-STATS-03** An empty cell is a missing value: it is skipped for min, max
  and mean, does not make a column text, and is not counted in `count`.
  (Not true in the code today — see *Known to be wrong today*.)

## Glossary
| Term | Meaning |
|---|---|
| Column kind | `number` (every non-empty cell parses as a number) or `text` |
| Summary | One row of output for a column: kind, count, and the stats for its kind |
| Missing value | An empty cell (BR-STATS-03) |

## Deeper docs
- `README.md` — usage and development setup.
