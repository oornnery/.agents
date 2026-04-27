---
name: polars
description: Polars DataFrame patterns for Python data processing. Covers the
  expression API, lazy evaluation, grouping, joins, window functions, CSV and
  Parquet I/O, performance, and pandas migration guidance.
---

# Polars

Use skill when work primarily Polars DataFrames, lazy pipelines, or high-performance tabular data processing in Python.

## Boundary

Use for:

- DataFrame and LazyFrame workflows
- expression-based transforms
- joins, aggregations, reshaping
- CSV, Parquet, NDJSON, database reads
- performance-sensitive data pipelines
- pandas-to-polars migration decisions

Pair with:

- `python` for project workflow, typing, general Python conventions
- `quality` when data transforms need tighter regression checks
- `docs` when data contracts, schemas, or pipeline behavior must be documented

## Reference Map

- `references/concepts.md` -- expressions, strict types, null handling, lazy vs eager mental model
- `references/operations.md` -- select, filter, with_columns, group_by, window functions, joins, concatenation, reshaping
- `references/io-and-performance.md` -- CSV and Parquet workflows, scan vs read, type choices, performance guardrails
- `references/pandas.md` -- conceptual and mechanical migration guidance from pandas to Polars

## Assets

- `assets/main.py` -- runnable entrypoint: reads local data, joins dimensions, writes derived report
- `assets/sales.csv` -- fact-style input data for example pipeline
- `assets/regions.csv` -- small dimension data for example join

## What Stays Here

Keep this file focused on defaults and guardrails.

- keep here: when prefer lazy mode, expression-first style, review cues
- move to refs: long API catalogs, migration tables, deeper I/O examples
- use assets when runnable example clearer than another code block

## Core Defaults

- prefer expression API over Python row-wise logic
- prefer `scan_*` plus `.collect()` for large or multi-step pipelines
- filter and select early in lazy pipelines
- use `with_columns()` for parallel column transforms
- keep joins explicit about keys and suffixes
- choose strict types on ingest when schema quality matters
- use Parquet over CSV when you control storage format
- keep pandas habits out of Polars where they fight execution model

## Lazy vs Eager

Prefer eager when:

- dataset small
- quick exploration
- workflow short and interactive

Prefer lazy when:

- data large
- chaining several steps
- only need some columns or rows
- performance matters enough to benefit from optimization

## Performance Rules

- do not reach for `map_elements()` when expression exists
- do not materialize intermediate frames unless needed
- do not load full CSVs eagerly to filter immediately
- do not leave string columns as generic text if categorical or temporal types more correct
- do not guess about bottlenecks; inspect plans and measure first

For deeper guidance, load `references/io-and-performance.md`.

## Guardrails

- keep transforms columnar and vectorized
- keep schema assumptions explicit at boundaries
- keep joins narrow and intentional; do not join giant tables casually
- keep null handling deliberate, not accidental conversions
- keep heavy business logic out of DataFrame expressions when it belongs in Python orchestration
- keep output schemas stable if downstream consumers depend on them

## Review Focus

- check whether lazy mode should replace eager reads
- check whether filters and projections happen early enough
- check whether expressions can replace Python callbacks
- check whether joins, null handling, casts are explicit
- check whether output schema stable and intentional
