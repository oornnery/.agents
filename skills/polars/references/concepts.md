# Polars Concepts

## Expressions First

Expressions are the core of Polars.

Use:

```python
pl.col('value') * 2
```

instead of thinking in row-by-row Python loops.

Expressions become useful inside contexts like:

- `select()`
- `with_columns()`
- `filter()`
- `group_by().agg()`

## Lazy vs Eager

### Eager

```python
df = pl.read_csv('data.csv')
result = df.filter(pl.col('age') > 25)
```

Use eager mode for:

- small frames
- one-off transforms
- notebook exploration

### Lazy

```python
lf = pl.scan_csv('data.csv')
result = lf.filter(pl.col('age') > 25).select('name', 'age')
df = result.collect()
```

Use lazy mode for:

- larger data
- multi-step pipelines
- performance-sensitive work

Benefits:

- predicate pushdown
- projection pushdown
- query optimization
- better execution planning

## Data Types

Polars is strict about types, which is usually a good thing.

Prefer:

- smaller integer types when the range is known
- `Date` or `Datetime` instead of free-form strings
- `Categorical` for repeated low-cardinality strings
- explicit casts when the contract changes

## Null Handling

Nulls are first-class.

```python
df.filter(pl.col('value').is_null())
df.with_columns(pl.col('value').fill_null(0))
df.drop_nulls(subset=['important_col'])
```

Do not assume Polars will silently coerce or fill missing values the way pandas
often does.

## Expression Composition

Store reusable expressions when they clarify the pipeline:

```python
price_with_tax = (pl.col('price') * 1.1).alias('price_with_tax')

df.select('name', price_with_tax)
```

This helps keep larger transforms readable.

## Window Functions

Use `over()` when you want group-aware calculations without collapsing rows:

```python
df.with_columns(
    avg_salary=pl.col('salary').mean().over('department'),
    rank_in_team=pl.col('score').rank().over('team'),
)
```

## Guardrails

- do not treat Polars like pandas with different syntax
- do not hide schema issues under eager ad hoc fixes
- do not use `Object` dtype unless there is no reasonable alternative
