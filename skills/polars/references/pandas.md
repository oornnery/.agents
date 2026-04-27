# Pandas Migration

## Mental Shift

Polars != pandas with different method names.

Key shifts:

- no general index-centric model
- stronger types
- expression-first transforms
- lazy execution available
- better default parallelism

## Common Translations

### Filter

Pandas:

```python
df[df['age'] > 25]
```

Polars:

```python
df.filter(pl.col('age') > 25)
```

### Add Column

Pandas:

```python
df['double'] = df['value'] * 2
```

Polars:

```python
df.with_columns(double=pl.col('value') * 2)
```

### Group By

Pandas:

```python
df.groupby('team')['score'].mean()
```

Polars:

```python
df.group_by('team').agg(pl.col('score').mean())
```

### Transform / Window

Pandas:

```python
df.groupby('team')['score'].transform('mean')
```

Polars:

```python
df.with_columns(pl.col('score').mean().over('team'))
```

## Migration Advice

- migrate one pipeline at time
- write regression tests around output schema and values
- use lazy mode where pandas pipelines were slow or memory-heavy
- do not port `apply` habits blindly; look for native expressions first

## Guardrails

- do not emulate pandas index patterns that Polars does not need
- do not assume sequential assignment semantics inside `with_columns()`
- do not accept silent schema drift during migration
