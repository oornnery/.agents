# SQLModel Query Patterns and Optimization

Use when query count, relationship loading, or DB performance matters.

## Basic Query Patterns

```python
from sqlmodel import select

statement = select(User)
users = session.exec(statement).all()

statement = select(User).where(User.id == user_id)
user = session.exec(statement).first()
```

Keep basic queries explicit, composable.

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

Prefer explicit filter composition over helpers that obscure query shape.

## Ordering and Pagination

```python
statement = select(User).order_by(User.created_at.desc())

statement = select(User).offset(skip).limit(limit)
```

Use cursor-style pagination for large or append-heavy datasets.

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

Keep heavy joins/aggregations near repository or persistence layer. Don't scatter through handlers.

## Subqueries and CTEs

Use subqueries/CTEs when they simplify complex filtering or aggregation. Keep named and isolated for reviewability.

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

- `selectinload` for collections in most app code
- `joinedload` when join shape is simple, row explosion acceptable
- Make loading strategy explicit in async code

## Nested Eager Loading

```python
statement = (
    select(User)
    .options(selectinload(User.posts).selectinload(Post.comments))
)
```

Beware nested eager loading on large graphs -- can over-fetch.

## Bulk Operations

- Use bulk inserts/updates/deletes when row count is high
- Avoid per-row loops when set-based op exists
- Measure transaction size and lock impact before bulk changes in prod

## Raw SQL

Use raw SQL only when:

- ORM expression becomes unreadable
- DB feature not exposed cleanly through normal query building
- Performance or explainability clearly improves

When using raw SQL:

- Keep parameterized
- Keep local to persistence layer
- Explain why ORM path wasn't used

## Query Profiling and Testing

For slow queries:

- Enable SQL logging selectively
- Capture actual query count
- Run `explain` or `explain analyze` in safe env
- Verify indexes match real filters and sort order

Test:

- Query count for critical list endpoints
- Relationship-heavy reads for N+1 regressions
- Pagination on realistic datasets
- Expensive aggregations and back-office screens

## Checklist

- [ ] loading strategy is explicit
- [ ] N+1 is prevented on relationship-heavy reads
- [ ] pagination matches dataset size
- [ ] indexes support real filters and orderings
- [ ] bulk ops replace row-by-row loops when needed
- [ ] raw SQL is parameterized and justified
- [ ] performance work is based on measurement
