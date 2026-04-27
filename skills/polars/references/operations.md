# Polars Operations

## Select and With Columns

`select()` changes shape. `with_columns()` keeps existing columns.

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

Multiple filter arguments for simple `AND` conditions.

## Group By and Aggregation

```python
df.group_by('department').agg(
    pl.col('salary').mean().alias('avg_salary'),
    pl.len().alias('count'),
)
```

- `pl.len()` for row counts
- explicit aliases for outputs
- grouped aggregations over Python post-processing

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

Keep conditions readable. Pull repeated sub-expressions into variables.

## Joins

```python
left.join(right, on='id', how='left')
left.join(other, left_on='user_id', right_on='id', how='inner')
```

Common join types: `inner`, `left`, `full`, `semi`, `anti`, `cross`

Explicit suffixes when columns overlap.

## Concatenation

```python
pl.concat([df1, df2], how='vertical')
pl.concat([df1, df2], how='horizontal')
pl.concat([df1, df2], how='diagonal')
```

- `vertical` -- same-schema row stacking
- `horizontal` -- column stacking, equal row counts
- `diagonal` -- schemas differ

## Pivot and Unpivot

Pivot: distinct values become columns. Unpivot: wide data becomes long.

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

Use over join-back patterns for per-row group context.

## Guardrails

- do not chain opaque transforms without aliases or intermediate naming
- do not use Python loops for expression-level work
- do not let joins/pivots silently reshape schema without review
