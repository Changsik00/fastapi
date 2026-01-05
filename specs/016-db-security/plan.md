# Plan: DB Security (Role Separation)

## Goal
Secure the database by creating distinct users for Application (DML) and Migration (DDL) usage.

## Proposed Changes

### 1. SQL Scripts
#### [NEW] [scripts/init_roles.sql](file:///Users/ck/Project/Changsik/fastapi/scripts/init_roles.sql)
- **Roles**:
    - `app_user`: The restricted user for the backend API.
    - `migration_user`: The privileged user for Alembic migrations.
- **Grants**:
    - `app_user`: `SELECT, INSERT, UPDATE, DELETE` on `public` tables.
    - `migration_user`: `ALL PRIVILEGES` on `public` tables and schema (Owner permissions).
- **Default Privileges**:
    - Ensure `app_user` automatically gets access to *future* tables created by `migration_user`.

### 2. Documentation
#### [NEW] [docs/db-security-setup.md](file:///Users/ck/Project/Changsik/fastapi/docs/db-security-setup.md)
- Guide on running the script in Supabase SQL Editor.
- Guide on updating `.env` (local and production) and GitHub Secrets.

## Verification Plan
### Manual Verification
1.  **Run Script**: Execute `init_roles.sql` (after replacing placeholders) on a local/test DB.
2.  **Test DML**: Connect as `app_user` and try to `SELECT` and `INSERT`. (Should Succeed)
3.  **Test DDL Block**: Connect as `app_user` and try to `DROP TABLE items`. (Should Fail)
4.  **Test Migration**: Connect as `migration_user` and try to `ALTER TABLE`. (Should Succeed)

## Decisions & Issues Log
| ID | Decision | Rationale | Status |
|----|----------|-----------|--------|
| | | | |
