# Spec: DB Security (Role Separation)

## 1. Background
Currently, the application connects to the database (PostgreSQL/Supabase) potentially using a superuser or owner account. This poses a security risk where an SQL injection vulnerability or accidental misconfiguration could lead to catastrophic table deletion or schema corruption.

## 2. Objective
Implement the "Least Privilege" principle by separating database roles:
1.  **Migration User (`migration_user`)**: Has DDL (Data Definition Language) privileges (CREATE, DROP, ALTER). Used *only* for CI/CD deployments/migrations.
2.  **Application User (`app_user`)**: Has DML (Data Manipulation Language) privileges (SELECT, INSERT, UPDATE, DELETE). Used by the running application.

## 3. Requirements
- **Supabase Compatibility**: Must work within Supabase's PostgreSQL environment.
- **Role Creation**:
    - `migration_user`: Can manage schema (`alembic`).
    - `app_user`: Can only read/write data in `public` schema. Cannot drop tables.
- **Verification**:
    - The `app_user` must be blocked from running `DROP TABLE items`.
- **Environment config**:
    - Provide instructions on how to update `.env` to use these new credentials.

## 4. Scope
- **In Scope**:
    - SQL script (`scripts/init_roles.sql`) to create users and grant permissions.
    - Updates to `docs/db-migration-policy.md` (or new doc) explaining usage.
- **Out of Scope**:
    - Automatic rotation of passwords (too complex for now).
    - Implementing this in Production *right now* (we provide the tools/docs, user executes).
