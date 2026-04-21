---
name: polars
description: Polars DataFrame patterns for Python data processing. Covers the
  expression API, lazy evaluation, grouping, joins, window functions, CSV and
  Parquet I/O, performance, and pandas migration guidance.
---

# Polars

Use this skill when the work is primarily Polars DataFrames, lazy pipelines, or
high-performance tabular data processing in Python.

## Boundary

Use this skill for:

- DataFrame and LazyFrame workflows
- expression-based transforms
- joins, aggregations, and reshaping
- CSV, Parquet, NDJSON, and database reads
- performance-sensitive data pipelines
- pandas-to-polars migration decisions

Pair with:

- `python` for project workflow, typing, and general Python conventions
- `quality` when data transformations need tighter regression checks
- `docs` when data contracts, schemas, or pipeline behavior must be documented

## Reference Map

- `references/concepts.md` -- expressions, strict types, null handling, and
  lazy vs eager mental model
- `references/operations.md` -- select, filter, with_columns, group_by, window
  functions, joins, concatenation, and reshaping
- `references/io-and-performance.md` -- CSV and Parquet workflows, scan vs
  read, type choices, and performance guardrails
- `references/pandas.md` -- conceptual and mechanical migration guidance from
  pandas to Polars

## Assets

- `assets/main.py` -- a runnable entrypoint that reads local data, joins
  dimensions, and writes a derived report
- `assets/sales.csv` -- fact-style input data for the example pipeline
- `assets/regions.csv` -- small dimension data used by the example join

## What Stays Here

Keep this file focused on defaults and guardrails.

- keep here: when to prefer lazy mode, expression-first style, and review cues
- move to refs: long API catalogs, migration tables, and deeper I/O examples
- use assets when a runnable example is clearer than another code block

## Core Defaults

- prefer the expression API over Python row-wise logic
- prefer `scan_*` plus `.collect()` for large or multi-step pipelines
- filter and select as early as possible in lazy pipelines
- use `with_columns()` for parallel column transforms
- keep joins explicit about keys and suffixes
- choose strict types on ingest when schema quality matters
- use Parquet over CSV when you control the storage format
- keep pandas habits out of Polars where they fight the execution model

## Lazy vs Eager

Prefer eager mode when:

- the dataset is small
- you are doing quick exploration
- the workflow is short and interactive

Prefer lazy mode when:

- data is large
- you are chaining several steps
- you only need some columns or rows
- performance matters enough to benefit from optimization

## Performance Rules

- do not reach for `map_elements()` when an expression exists
- do not materialize intermediate frames unless you need them
- do not load full CSVs eagerly just to filter them immediately
- do not leave string columns as generic text if categorical or temporal types
  are more correct
- do not guess about bottlenecks; inspect plans and measure first

For deeper guidance, load `references/io-and-performance.md`.

## Guardrails

- keep transformations columnar and vectorized
- keep schema assumptions explicit at boundaries
- keep joins narrow and intentional; do not join giant tables casually
- keep null handling deliberate instead of relying on accidental conversions
- keep heavy business logic out of DataFrame expressions when it belongs in
  Python orchestration
- keep output schemas stable if downstream consumers depend on them

## Review Focus

- check whether lazy mode should replace eager reads
- check whether filters and projections happen early enough
- check whether expressions can replace Python callbacks
- check whether joins, null handling, and casts are explicit
- check whether the output schema is stable and intentional
