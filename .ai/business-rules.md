# Business rules

<!-- The full list of rules the product must always follow. Intake, planner and
     reviewer check every change against it. Each rule has a stable ID:
     BR-<AREA>-<nn>. Never reuse or renumber an ID; retire a rule by marking it
     "Retired (#issue)".

     When a change ships, the rules it adds or changes are written here, in the
     same PR. Acceptance criteria name the rules they depend on: AC-1 [BR-PRICE-01].

     .ai/steering/product.md lists the few rules every change must respect and
     links here for the rest. -->

## Rules

| ID | Rule | Source | Verified in code |
|---|---|---|---|
| BR-STATS-01 | A number column is summarised with its min, max and mean. | `README.md` | `src/tally/stats.py` `summarise_column` |
| BR-STATS-02 | A text column is summarised with its number of distinct values. | `README.md` | `src/tally/stats.py` `summarise_column` |
| BR-STATS-03 | An empty cell is a missing value: it is skipped for min, max and mean, it does not turn a number column into text, and `count` counts only non-empty cells. | prinveee, project setup 2026-11-08 | Broken today — see below |

## Known to be wrong today
<!-- Where the code breaks a rule above. Each is a bug waiting for an issue. -->
| Rule | What the code does instead | Issue |
|---|---|---|
| BR-STATS-03 | `_as_numbers` fails on `""`, so one empty cell makes the whole column `text`; `count` is `len(values)` including empty cells. `examples/orders.csv` shows it: `items` (`2,1,,3`) comes out as text, count 4, distinct 4. | none yet |

## Open questions
<!-- Rules nobody has decided yet. Agents never guess these: they ask. -->
| # | Question | Who can answer |
|---|---|---|
| 1 | A column whose cells are all empty: which kind is it (`number`, `text`, or something else), and what does its row show? | prinveee |
| 2 | In a text column, is an empty cell skipped for `distinct` too (BR-STATS-03 says it is a missing value, but only names min/max/mean and count)? | prinveee |
| 3 | `nan` and `inf` parse as numbers today and flow into min/max/mean. Should they? | prinveee |
| 4 | A file that is not valid UTF-8 crashes with a traceback; should it exit 2 with a `tally:` message like a missing file? | prinveee |
| 5 | Is exit code 2 for a missing file a promise to users (it is tested in `tests/test_cli.py`, not documented)? | prinveee |
