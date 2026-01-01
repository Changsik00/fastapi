# Specification: Real Database (PostgreSQL)

## 1. Goal
Replace the in-memory data store with a persistent **PostgreSQL** database using **SQLModel**.

## 2. Background
The project currently uses an in-memory dictionary for storage, which loses data on restart. We need to implement a persistent database layer. The user has provided a Supabase PostgreSQL instance.

## 3. Requirements

### Functional Requirements
- **Persistence**: Data must be stored in PostgreSQL.
- **ORM**: Use `SQLModel` for schema definition and database interactions.
- **Async**: Use async driver (`asyncpg`) for non-blocking database operations.
- **Configuration**: Connection string must be loaded from `DATABASE_URL` in `.env`.
- **Repository**: Created items must be retrievable after server restart.

### Non-Functional Requirements
- **Security**: Database credentials MUST NOT be committed to git. Use `.env`.
- **Architecture**:
    - Infrastructure layer: `PostgresItemRepository`.
    - Domain layer: Update models if necessary/compatible with SQLModel.
    - Service layer: Should remain largely unchanged (Interface segregation).

## 4. User Stories
- **Developer**: I can set `DATABASE_URL` in `.env` and the app connects to it automatically.
- **User**: When I create an item and restart the server, the item is still there.

## 5. Mockups
`.env`:
```bash
DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/dbname"
```
