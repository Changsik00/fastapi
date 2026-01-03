# Plan: Dependency Injection Refactoring

## 1. Architecture

We will introduce a central dependency module `app/api/deps.py` to manage the injection graph.

### The Dependency Chain
1.  **Database Session**: `get_session` (yields `AsyncSession`).
2.  **Repository**: `get_item_repository` (depends on `get_session`, returns `ItemRepository` interface with `PostgresItemRepository` implementation).
3.  **Service**: `get_item_service` (depends on `get_item_repository`, returns `ItemService`).

### File Structure Changes
- **[NEW]** `app/api/deps.py`: Contains the dependency functions.
- **[MODIFY]** `app/api/v1/items.py`: Replace manual instantiation with `Depends`.

## 2. Implementation Steps

### Step 1: Create `app/api/deps.py`
Define the dependency providers:
```python
async def get_db() -> AsyncGenerator[AsyncSession, None]: ...
async def get_item_repository(session: AsyncSession = Depends(get_db)) -> ItemRepository: ...
async def get_item_service(repo: ItemRepository = Depends(get_item_repository)) -> ItemService: ...
```

### Step 2: Refactor `app/api/v1/items.py`
Update endpoints to inject the service:
```python
@router.post("/", response_model=Item)
async def create_item(
    item: ItemCreate,
    service: ItemService = Depends(get_item_service) # Injected!
):
    return await service.create_item(item)
```

### Step 3: Cleanup
- Remove ad-hoc `get_session` imports in routes if simpler.
- Ensure `main.py` is clean.

## 3. Verification
- **Application**: Run manual test via Swagger UI.
- **Tests**: Run `pytest`.
    - Note: `tests/conftest.py` currently overrides `get_session`. This should seamlessly propagate through the new dependency chain (`get_db` -> `get_item_repository`). We will verify this works without modifying test code.
