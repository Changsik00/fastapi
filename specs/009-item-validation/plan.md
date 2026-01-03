# Plan: Item Model Validation

## 1. Architecture
We will modify the existing `ItemBase` model (or `ItemCreate` / `ItemUpdate` specifically) in `app/domain/models/item.py`.
Since `Item` inherits from `ItemBase`, validation rules on `ItemBase` will apply to all derived models, which is efficient.

## 2. Implementation Steps

### Step 1: Define Regex
- Define a regex pattern for "Alphanumeric (English+Korean) + Space": `^[a-zA-Z0-9가-힣 ]+$`.

### Step 2: Add Validators to `ItemBase`
- **Field Constraints**: Update `name: str = Field(...)` to include `min_length=2`, `max_length=50`.
- **Custom Validator (`@field_validator("name")`)**:
    1.  Check forbidden words ("admin", "root").
    2.  Check special characters (using regex).
    3.  Check not empty/whitespace only.

### Step 3: Tests
- Create `tests/unit/test_item_validation.py` (New Unit Test).
- We don't need to hit the DB or API to test Pydantic models. Unit tests are faster.
- **Cases**:
    - Valid name: "Apple", "Blue Car"
    - Invalid length: "A", "Very long name..."
    - Invalid chars: "Apple!", "N@me"
    - Forbidden: "admin"

## 3. Database Schema Migration (Updates)
Since we added `max_length` to `Field`, we should reflect this in the database schema to prevent direct SQL inserts of invalid data.
1.  Run `uv run alembic revision --autogenerate -m "Apply length constraints to item table"`
2.  Run `uv run alembic upgrade head`

## 4. Verification
- `pytest tests/unit/test_item_validation.py`
- Check `alembic` output to ensure `VARCHAR(50)` is applied.
