# Specification: Dependency Injection Refactoring

## 1. Goal
Refactor the application to use FastAPI's dependency injection system (`Depends`) consistently across all layers. This will remove manual instantiation of services and repositories in `main.py` or API routers, ensuring better testability and loose coupling.

## 2. Background
Currently, `api/v1/items.py` or `main.py` manually composes the dependency chain (e.g., `repo = PostgresItemRepository(session)`). This makes unit testing (mocking) harder and violates FastAPI best practices.

## 3. Requirements
1.  **Session Injection**: Ensure `get_session` is used via `Depends`.
2.  **Repository Injection**: Create a `get_item_repository` dependency that provides `ItemRepository`.
3.  **Service Injection**: Create a `get_item_service` dependency that provides `ItemService` (injecting the repo).
4.  **Route Refactoring**: Update `api/v1/items.py` to inject `ItemService` directly.
5.  **Main Refactoring**: Ensure `main.py` is clean of business logic instantiation.

## 4. Architecture Change
- **Before**: Router manually calls `PostgresItemRepository(session)`.
- **After**: Router defines `service: ItemService = Depends(get_item_service)`. FastAPI handles the rest.

## 5. Verification
- `pytest` must pass (creating mocks/overrides if necessary).
- `README.md` should reflect DI patterns if needed.
