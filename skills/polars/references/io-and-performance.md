# Polars I/O and Performance

## Read vs Scan

Use `read_*` for eager loading and `scan_*` for lazy pipelines.

```python
df = pl.read_csv('data.csv')
lf = pl.scan_parquet('data.parquet')
```

Prefer `scan_*` when:

- files are large
- you will filter or select immediately
- the pipeline has multiple steps

## CSV

```python
pl.read_csv(
    'data.csv',
    schema_overrides={
        'id': pl.UInt32,
        'created_at': pl.Date,
    },
)
```

Be explicit with schema overrides when:

- type inference is flaky
- correctness matters more than convenience
- you want smaller or better types

## Parquet

Prefer Parquet when you control the format:

- smaller files
- faster reads
- columnar efficiency
- better pushdown behavior

```python
df.write_parquet('output.parquet')
lf = pl.scan_parquet('output.parquet')
```

## NDJSON and Other Formats

Use NDJSON when streaming line-oriented JSON is a better fit than arrays.

```python
df = pl.read_ndjson('events.ndjson')
```

## Database Reads

Keep database ingestion narrow:

- select only required columns
- filter early in SQL when that is the real boundary
- avoid using Polars as a substitute for poor upstream query shape

## Performance Rules

- filter early
- project early
- avoid Python UDFs unless unavoidable
- avoid repeated collects in the middle of a lazy pipeline
- rechunk after large concatenations when later work benefits

## Anti-Patterns

Bad:

- eager read -> huge transform -> final filter
- `map_elements()` for simple math or string operations
- untyped CSV ingestion in critical paths
- joining wide tables before pruning columns

Better:

- scan -> filter -> select -> transform -> collect

## Measurement

Measure before optimizing:

- inspect query plans
- compare lazy and eager behavior
- verify schema and null changes in tests
- benchmark real workloads, not toy slices
