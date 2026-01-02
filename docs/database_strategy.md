# Database Strategy: SQLModel, Alembic, and Asyncpg

This document explains the architectural decisions behind our database stack.

## 1. Why Alembic? (Migration Management)

We chose **Alembic** to manage database migrations for the following critical reasons:

### 1. Data Preservation & Incremental Changes
`SQLModel.metadata.create_all()` only creates missing tables. It cannot handle modifications (e.g., adding a column) to existing tables without data loss. Alembic detects changes (Diff) and generates scripts to apply them while preserving data.

### 2. Version Control & Rollback
Alembic treats DB state like code:
- **History**: Tracks who changed what and when.
- **Rollback**: Allows safely reverting to a previous version (`downgrade`) if a deployment fails.

### 3. Collaboration & Environment Consistency
Ensures all developers and environments (Dev, Test, Prod) share the exact same schema. Running `alembic upgrade head` synchronizes the local DB with the codebase.

### 4. Autogenerate (Productivity)
Alembic compares `SQLModel` code with the actual DB to automatically generate migration scripts (`alembic revision --autogenerate`). This reduces manual SQL writing and errors.

### 5. Production Safety
In production, dropping tables is not an option. Alembic provides the standard, safe workflow for evolving the schema without downtime.

---

## 2. What is asyncpg? (Async Driver)

**asyncpg** is a high-performance PostgreSQL driver for Python's `asyncio`.

### 1. Performance
It interacts directly with PostgreSQL's binary protocol, offering significantly higher performance (often 5x faster) than traditional drivers like `psycopg2`.

### 2. Full Async Support
It allows non-blocking database I/O, which is essential for FastAPI's high-concurrency model. The CPU can handle other requests while waiting for DB queries to return.

---

## 3. The Trinity: SQLModel + Alembic + asyncpg

We combine these three tools to create a robust, high-performance stack:

| Tool | Role | Analogy |
|------|------|---------|
| **SQLModel** | Data Structure & Queries | Blueprint / Spec |
| **Alembic** | Schema Change Management | Git for Database |
| **asyncpg** | High-speed Async Communication | Dedicated Express Line |

### How they interact in this project:
- **Execution**: `SQLModel` uses `sqlalchemy.ext.asyncio` + `asyncpg` to execute queries (CRUD).
- **Migration**: `Alembic` (configured with `async` template) shares the same `asyncpg` driver to inspect and upgrade the database.
