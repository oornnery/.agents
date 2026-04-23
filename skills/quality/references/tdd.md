# TDD

Use TDD when tests should drive design, not validate after.

> Write test first. Fail. Pass. Clean up.

## The Cycle

```text
RED -> GREEN -> REFACTOR -> repeat
```

1. **Red** -- write failing test for one behavior
2. **Green** -- write minimum code to pass
3. **Refactor** -- improve structure, keep behavior

Each cycle: minutes, not hours. Longer = step too big.

## Core Rules

- write test before implementation
- one red test at a time
- smallest code that passes
- refactor only on green
- hard test = design wants simplification

## Session Workflow

1. define interface or next behavior
2. write one failing test
3. confirm fails for right reason
4. implement smallest pass
5. refactor on green
6. run broader relevant suite

## Commands

```bash
uv run pytest --lf -x -v
uv run pytest tests/unit/test_<module>.py::test_<name> -x -v
uv run pytest -v
uv run pytest --cov=src --cov-report=term-missing -v
```

## Arrange / Act / Assert

```python
def test_expired_token_returns_401(client):
    token = create_token(expired=True)

    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
```

Keep each section short. Arrange growing too large = extract fixture.

## BDD

Use Given / When / Then naming when it improves clarity:

```python
def test_given_empty_cart_when_checkout_then_raises_error(cart_service):
    cart = cart_service.create_cart(user_id="user-1")

    with pytest.raises(EmptyCartError):
        cart_service.checkout(cart.id)
```

Simpler cases: behavior-first names:

```python
def test_create_user_returns_201(): ...
```

## Acceptance Criteria Mapping

Map formal acceptance criteria directly to tests:

```python
def test_ac01_search_users_by_name(client, sample_users): ...
def test_ac02_empty_search_returns_paginated_results(client, sample_users): ...
def test_ac03_invalid_search_input_returns_422(client): ...
```

## API TDD

Test contract before writing endpoint:

```python
def test_create_user(client):
    response = client.post("/api/users", json={"name": "Alice", "email": "a@b.co"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data
```

Recommended order:

- happy path
- validation failures
- edge cases
- refactor

## What to Test

- business logic and domain rules
- edge cases: empty input, `None`, boundaries, max values
- error paths and invalid states
- API/contract behavior at system boundaries
- integration points where data shape or side effects matter

## Anti-Patterns

- testing implementation not behavior
- tests after code
- steps too large
- over-mocking
- multiple failing tests at once
- coverage as replacement for thinking

## When Not to Use TDD

- prototyping spikes before design stabilizes
- generated code
- trivial wiring already covered elsewhere