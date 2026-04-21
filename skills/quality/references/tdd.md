# TDD

Use TDD when you want tests to drive the design instead of validating it after
the fact.

> Write the test first. Let it fail. Make it pass. Clean up.

## The Cycle

```text
RED -> GREEN -> REFACTOR -> repeat
```

1. **Red** -- write a failing test that describes one behavior
2. **Green** -- write the minimum code to make that test pass
3. **Refactor** -- improve structure without changing behavior

Each cycle should take minutes, not hours. If it takes longer, the step is too
big.

## Core Rules

- write the test before the implementation
- keep one red test at a time
- write the smallest code that makes it pass
- refactor only while tests stay green
- if a test is hard to write, the design probably wants simplification

## Session Workflow

1. define the interface or next behavior
2. write one failing test
3. confirm it fails for the right reason
4. implement the smallest pass
5. refactor on green
6. run a broader relevant suite

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

Keep each section short. If Arrange grows too large, extract a fixture.

## BDD

Use Given / When / Then naming when it improves clarity:

```python
def test_given_empty_cart_when_checkout_then_raises_error(cart_service):
    cart = cart_service.create_cart(user_id="user-1")

    with pytest.raises(EmptyCartError):
        cart_service.checkout(cart.id)
```

Simpler cases can use behavior-first names:

```python
def test_create_user_returns_201(): ...
```

## Acceptance Criteria Mapping

Map formal acceptance criteria directly to tests when useful:

```python
def test_ac01_search_users_by_name(client, sample_users): ...
def test_ac02_empty_search_returns_paginated_results(client, sample_users): ...
def test_ac03_invalid_search_input_returns_422(client): ...
```

## API TDD

Test the contract before writing the endpoint:

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
- edge cases such as empty input, `None`, boundaries, and max values
- error paths and invalid states
- API and contract behavior at system boundaries
- integration points where data shape or side effects matter

## Anti-Patterns

- testing implementation instead of behavior
- writing tests after code
- steps that are too large
- over-mocking
- multiple failing tests at once
- treating coverage as a replacement for thinking

## When Not to Use TDD

- prototyping spikes before the design stabilizes
- generated code
- trivial wiring already covered elsewhere
