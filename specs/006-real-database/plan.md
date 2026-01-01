# Plan: Real Database (PostgreSQL)

## 1. Architecture
We will introduce a proper database connection lifecycle using **SQLModel**.

### Components
- **`app/core/database.py`**: Manages `create_async_engine` and `get_session`.
- **`app/domain/models/item.py`**: Update `Item` model to be a `SQLModel` table.
- **`app/infrastructure/repositories/postgres_item_repository.py`**: New repository implementation using SQLModel Session.
- **`app/main.py`**: Adjust dependency injection to use the new repository.

## 2. Dependencies
- `sqlmodel`: The ORM.
- `asyncpg`: PostgreSQL async driver.
- `greenlet`: Required by SQLAlchemy for async operations.

## 3. Data Schema
`Item` model will become a table:
```python
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
```

## 4. Implementation Steps

### 1. Setup
- Install dependencies (`sqlmodel`, `asyncpg`, `greenlet`).
- Verify `.env` has valid `DATABASE_URL` (Done).

### 2. Core Implementation
- **`database.py`**: Implement `AsyncEngine` and `get_db` dependency.
- **`models/item.py`**: Inherit from `SQLModel`, set `table=True`.

### 3. Repository
- Implement `PostgresItemRepository` implementing `ItemRepository`.
- Use `AsyncSession` to perform CRUD operations.

### 4. Integration
- **`main.py`**: on_startup event to creating tables (`target_metadata.create_all`).
- Update `get_item_repository` dependency to return `PostgresItemRepository`.

## 5. Verification
- **Automated**: Run `pytest`. Note: `InMemory` tests might need adjustment or we separate Unit/Integration tests.
    - *Strategy*: For now, we will replace the repository implementation. We should ideally create a new test file `tests/integration/test_postgres_items.py` or mock the session for unit tests. To keep it simple for this step, we'll aim for functional parity.
- **Manual**: Start app, create item, restart server, check if item exists.
