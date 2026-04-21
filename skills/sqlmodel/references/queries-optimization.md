# SQLModel Query Patterns and Optimization

Use this reference when query count, relationship loading, or database
performance becomes important.

## Basic Query Patterns

```python
from sqlmodel import select

statement = select(User)
users = session.exec(statement).all()

statement = select(User).where(User.id == user_id)
user = session.exec(statement).first()
```

Keep basic queries explicit and composable.

## Filtering

```python
from sqlalchemy import or_
from sqlmodel import select

statement = select(User).where(User.is_active == True)

statement = select(User).where(
    User.is_active == True,
    User.email_verified == True,
)

statement = select(User).where(
    or_(User.email == "user@example.com", User.username == "user123")
)
```

Prefer explicit filter composition over helper functions that obscure query
shape.

## Ordering and Pagination

```python
statement = select(User).order_by(User.created_at.desc())

statement = select(User).offset(skip).limit(limit)
```

Use cursor-style pagination when datasets are large or append-heavy.

## Joins and Aggregations

```python
from sqlalchemy import func
from sqlmodel import select

statement = select(User, Post).join(Post, User.id == Post.user_id)

statement = (
    select(User.country, func.count(User.id))
    .group_by(User.country)
)
```

Keep heavy join and aggregation queries close to the repository or persistence
layer instead of scattering them through handlers.

## Subqueries and CTEs

Use subqueries and CTEs when they make complex filtering or aggregation easier
to reason about. Keep them named and isolated so they remain reviewable.

## N+1 Prevention

### Bad

```python
users = session.exec(select(User)).all()
for user in users:
    posts = user.posts
```

### Good with `selectinload`

```python
from sqlalchemy.orm import selectinload
from sqlmodel import select

statement = select(User).options(selectinload(User.posts))
users = session.exec(statement).all()
```

### Good with `joinedload`

```python
from sqlalchemy.orm import joinedload
from sqlmodel import select

statement = select(User).options(joinedload(User.posts))
users = session.exec(statement).unique().all()
```

Defaults:

- use `selectinload` for collections in most application code
- use `joinedload` when the join shape is simple and the row explosion is
  acceptable
- make loading strategy explicit in async code

## Nested Eager Loading

```python
statement = (
    select(User)
    .options(selectinload(User.posts).selectinload(Post.comments))
)
```

Be careful with nested eager loading on large graphs. It can still over-fetch.

## Bulk Operations

- use bulk inserts, updates, or deletes when row count is high
- avoid per-row loops when a set-based operation is available
- measure transaction size and lock impact before applying bulk changes in
  production

## Raw SQL

Use raw SQL only when:

- the ORM expression becomes unreadable
- the database feature is not exposed cleanly through normal query building
- performance or explainability clearly improves

When using raw SQL:

- keep it parameterized
- keep it local to the persistence layer
- explain why the ORM path was not used

## Query Profiling and Testing

For slow queries:

- enable SQL logging selectively
- capture actual query count
- run explain or explain analyze in a safe environment
- verify indexes match the real filters and sort order

Test:

- query count for critical list endpoints
- relationship-heavy reads for N+1 regressions
- pagination on realistic datasets
- expensive aggregations and back-office screens

## Checklist

- [ ] loading strategy is explicit
- [ ] N+1 is prevented on relationship-heavy reads
- [ ] pagination matches dataset size
- [ ] indexes support real filters and orderings
- [ ] bulk operations replace row-by-row loops when needed
- [ ] raw SQL is parameterized and justified
- [ ] performance work is based on measurement
