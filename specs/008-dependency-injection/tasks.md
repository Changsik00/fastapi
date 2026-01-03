# Tasks: Dependency Injection Refactoring

- [ ] **1. Create Dependency Module** <!-- id: 1 -->
    - Create `app/api/deps.py`.
    - Implement `get_session` (moved from `database.py` or imported).
    - Implement `get_item_repository` (Injects session).
    - Implement `get_item_service` (Injects repository).

- [ ] **2. Refactor Routes** <!-- id: 2 -->
    - Modify `app/api/v1/items.py`.
    - Remove direct instantiation of `PostgresItemRepository` and `ItemService`.
    - Use `Depends(get_item_service)` in route handlers.

- [ ] **3. Verification** <!-- id: 3 -->
    - Run `pytest`.
    - Verify `tests/conftest.py` still overrides `get_session` correctly (this is key, as `deps.py` will import `get_session` from `database.py`, which is what conftest overrides).
