# Polars Operations

## Select and With Columns

Use `select()` for shape-changing output and `with_columns()` when preserving
existing columns.

```python
df.select('name', 'age')

df.with_columns(
    age_plus_10=pl.col('age') + 10,
    name_upper=pl.col('name').str.to_uppercase(),
)
```

## Filter

```python
df.filter(pl.col('age') > 25)

df.filter(
    pl.col('age') > 25,
    pl.col('city') == 'NY',
)
```

Prefer multiple filter arguments for simple `AND` conditions.

## Group By and Aggregation

```python
df.group_by('department').agg(
    pl.col('salary').mean().alias('avg_salary'),
    pl.len().alias('count'),
)
```

Use:

- `pl.len()` for row counts
- explicit aliases for outputs
- grouped aggregations instead of Python post-processing

## Conditional Logic

```python
df.with_columns(
    grade=pl.when(pl.col('score') >= 90)
    .then('A')
    .when(pl.col('score') >= 80)
    .then('B')
    .otherwise('C'),
)
```

Keep conditions readable. Pull repeated sub-expressions into variables if
needed.

## Joins

```python
left.join(right, on='id', how='left')
left.join(other, left_on='user_id', right_on='id', how='inner')
```

Common join types:

- `inner`
- `left`
- `full`
- `semi`
- `anti`
- `cross`

Be explicit about suffixes if overlapping columns exist.

## Concatenation

```python
pl.concat([df1, df2], how='vertical')
pl.concat([df1, df2], how='horizontal')
pl.concat([df1, df2], how='diagonal')
```

Use:

- `vertical` for same-schema row stacking
- `horizontal` for column stacking with equal row counts
- `diagonal` when schemas differ

## Pivot and Unpivot

Use pivot when distinct values should become columns.
Use unpivot when wide data should become long.

```python
df.pivot(values='amount', index='customer', on='month')
df.unpivot(index='customer')
```

## Window Functions

```python
df.with_columns(
    avg_by_city=pl.col('age').mean().over('city'),
    running_total=pl.col('amount').cum_sum().over('account'),
)
```

Use these instead of join-back patterns when you need per-row group context.

## Guardrails

- do not chain many opaque transforms without aliases or intermediate naming
- do not use Python loops for work that belongs in expressions
- do not let joins and pivots silently reshape the schema without review
