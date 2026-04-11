---
name: tdd
description: Test-Driven Development methodology — Red/Green/Refactor cycle, BDD, test-first workflow. Load when writing tests before code, practicing TDD, or applying BDD patterns.
---

# Test-Driven Development

> _"Write the test first. Let it fail. Make it pass. Clean up."_

## The Cycle

```text
   RED           GREEN         REFACTOR
   ┌───┐         ┌───┐         ┌───┐
   │ Write test  │ Write code  │ Clean up
   │ that fails  │ to pass it  │ the code
   └─────────────┴─────────────┴───────┘
         ▲                          │
         └──────────────────────────┘
```

1. **Red** — Write a failing test that describes the behavior you want.
2. **Green** — Write the minimum code to make the test pass.
3. **Refactor** — Improve the code without changing behavior. Tests stay green.

Each cycle should take **minutes, not hours**. If it takes longer, the
step is too big — break it down.

## Rules

- Write the test **before** the implementation — no exceptions
- Each test describes **one behavior**, not one function
- Write the **simplest** code that makes the test pass — resist designing ahead
- Refactor only when tests are green
- Run tests after every change: `uv run pytest --lf -x`
- Never write new code without a failing test demanding it

## Test Structure: Arrange / Act / Assert

```python
def test_expired_token_returns_401(client):
    # Arrange — set up preconditions
    token = create_token(expired=True)

    # Act — perform the action under test
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})

    # Assert — verify the expected outcome
    assert response.status_code == 401
```

Keep each section short. If Arrange is long, extract a fixture.

## BDD — Behavior-Driven Development

BDD extends TDD with a ubiquitous language shared between developers,
testers, and stakeholders.

### Given / When / Then

```python
def test_given_empty_cart_when_checkout_then_raises_error(cart_service):
    # Given: an empty shopping cart
    cart = cart_service.create_cart(user_id="user-1")

    # When / Then: checkout raises an error
    with pytest.raises(EmptyCartError):
        cart_service.checkout(cart.id)
```

### Naming Convention

```python
# Pattern: test_given_<precondition>_when_<action>_then_<expected>
def test_given_valid_credentials_when_login_then_returns_token(): ...
def test_given_duplicate_email_when_register_then_returns_409(): ...
def test_given_no_stock_when_add_to_cart_then_returns_out_of_stock(): ...
```

For simpler cases, use behavior-first naming:

```python
# Pattern: test_<action>_<expected_result>
def test_create_user_returns_201(): ...
def test_search_with_empty_query_returns_all(): ...
def test_delete_nonexistent_returns_404(): ...
```

### Acceptance Criteria → Tests

Map SPEC.md acceptance criteria directly to test functions:

```markdown
## Acceptance Criteria (SPEC.md)

- [ ] AC-01: Users can search by name or email
- [ ] AC-02: Empty query returns all users (paginated)
- [ ] AC-03: Invalid input returns 422 with structured errors
```

```python
# tests/test_user_search.py — maps 1:1 to acceptance criteria

def test_ac01_search_users_by_name(client, sample_users): ...
def test_ac01_search_users_by_email(client, sample_users): ...
def test_ac02_empty_search_returns_paginated_results(client, sample_users): ...
def test_ac03_invalid_search_input_returns_422(client): ...
```

## TDD for APIs

Test the contract before writing the endpoint:

```python
# Step 1: RED — write the test
def test_create_user(client):
    response = client.post("/api/users", json={"name": "Alice", "email": "a@b.co"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data

# Step 2: GREEN — implement the minimum endpoint
# Step 3: REFACTOR — extract validation, add service layer
```

### API TDD Workflow

Happy path -> validation errors -> edge cases -> refactor.
Write test first for each, make it pass, then move to the next.

## TDD Workflow Commands

```bash
# Fast feedback loop — last failed, stop on first failure
uv run pytest --lf -x -v

# Watch mode (with pytest-watch)
uv run ptw -- --lf -x -v

# Run only the test you're working on
uv run pytest tests/test_users.py::test_create_user -v

# Coverage check after a TDD session
uv run pytest --cov=src --cov-report=term-missing -v
```

## Anti-Patterns

- Testing implementation instead of behavior -- breaks on every refactor.
- Writing tests after code -- misses edge cases.
- Large test steps -- break down into smaller increments.
- Over-mocking -- prefer fakes over mocks.
- Multiple failing tests at once -- one red test at a time.

## When NOT to Use TDD

- **Prototyping** -- write tests after the spike, before merging.
- **Generated code** -- migrations, serializers, boilerplate.
- **Trivial wiring** -- integration tests cover this.

## Related

- `skills/testing/SKILL.md` — test pyramid, fixtures, coverage, failure triage.
- `skills/architecture/SKILL.md` — domain-driven design testing patterns.
- `commands/plan.md` — writing SPEC acceptance criteria that map to tests.
