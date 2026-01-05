# Database Security Setup Guide

## Overview
This guide explains how to secure your Supabase/PostgreSQL database by implementing **Role Separation**.
This prevents the application from accidentally dropping tables or altering schemas.

## Roles
1.  **Migration User** (`postgres` or `migration_user`)
    -   **Permissions**: Full Admin (DDL + DML).
    -   **Usage**: CI/CD pipelines, Alembic migrations, Initial setup.
2.  **Application User** (`app_user`)
    -   **Permissions**: Read/Write (DML) only. (SELECT, INSERT, UPDATE, DELETE).
    -   **Usage**: The running FastAPI application.

## 🚀 Setup Instructions

### 1. Run the Role Script
1.  Open your **Supabase Dashboard** -> **SQL Editor**.
2.  Open the file `scripts/init_roles.sql` from this project.
3.  **IMPORTANT**: Replace `'YOUR_SECURE_PASSWORD'` in the script with a strong password.
4.  Run the script.

### 2. Configure Local Environment (`.env`)
Update your `.env` file to use the `app_user` for the application connection:
```ini
# For Application (DML)
DATABASE_URL=postgresql+asyncpg://app_user:NEW_PASSWORD@db.xxx.supabase.co:5432/postgres

# For Migrations (Keep this implicitly or use a separate env var if needed)
# Direct migrations usually use the admin credentials.
```

### 3. Configure Production (CI/CD)
1.  Go to GitHub Repository **Settings** -> **Secrets and variables** -> **Actions**.
2.  Ensure `DATABASE_URL` (if used for integration tests) is appropriate.
3.  If you have a separate `MIGRATION_DB_URL` secret, ensure it uses the **Admin** credentials (`postgres` user).

## Verification
To verify the setup, try running a destructive command as `app_user`:
```sql
-- Connect as app_user
DROP TABLE items;
-- result: ERROR: permission denied for schema public
```
