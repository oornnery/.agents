# Polars I/O and Performance

## Read vs Scan

Use `read_*` eager, `scan_*` lazy.

```python
df = pl.read_csv('data.csv')
lf = pl.scan_parquet('data.parquet')
```

Prefer `scan_*` when:

- files large
- filter/select immediate
- multi-step pipeline

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

- type inference flaky
- correctness > convenience
- want smaller/better types

## Parquet

Prefer Parquet when you control format:

- smaller files
- faster reads
- columnar efficiency
- better pushdown behavior

```python
df.write_parquet('output.parquet')
lf = pl.scan_parquet('output.parquet')
```

## NDJSON and Other Formats

Use NDJSON when streaming line-oriented JSON beats arrays.

```python
df = pl.read_ndjson('events.ndjson')
```

## Database Reads

Keep DB ingestion narrow:

- select only required columns
- filter early in SQL -- real boundary
- don't use Polars to mask poor upstream queries

## Performance Rules

- filter early
- project early
- avoid Python UDFs unless unavoidable
- avoid repeated collects mid-lazy pipeline
- rechunk after large concatenations when later work benefits

## Anti-Patterns

Bad:

- eager read -> huge transform -> final filter
- `map_elements()` for simple math/string ops
- untyped CSV ingestion in critical paths
- joining wide tables before pruning columns

Better:

- scan -> filter -> select -> transform -> collect

## Measurement

Measure before optimizing:

- inspect query plans
- compare lazy vs eager behavior
- verify schema/null changes in tests
- benchmark real workloads, not toy slices
