-- DB Role Separation Script (Supabase/PostgreSQL)
-- This script creates two roles:
-- 1. migration_user: Has full DDL privileges (for CI/CD and Alembic).
-- 2. app_user: Has DML privileges only (for the running application).
-- 3. readonly_user: Has SELECT privilege only (for developers/analysts).

-- Note: Replace 'YOUR_SECURE_PASSWORD' with actual strong passwords before running.
-- Note: In Supabase, you might need to run this in the SQL Editor.

-- 1. Create Migration User (Owner of the schema/tables)
-- This user is already effectively the 'postgres' user, but let's define explicit grants if we create a separate one.
-- For simplicity in Supabase, we often use the default 'postgres' as the migration user.
-- But here is how to create a restricted app_user.

-- Create app_user
CREATE USER app_user WITH PASSWORD 'YOUR_SECURE_PASSWORD';

-- Grant Connect
GRANT CONNECT ON DATABASE postgres TO app_user;

-- Grant Usage on Schema public
GRANT USAGE ON SCHEMA public TO app_user;

-- Grant DML privileges on all existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

-- Grant Usage on all sequences (for ID generation)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- IMPORTANT: Ensure future tables automatically grant privileges to app_user
-- This assumes 'postgres' (or whichever user runs migrations) is the one creating tables.
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO app_user;

-- Create readonly_user (For humans/developers to inspect data safely)
CREATE USER readonly_user WITH PASSWORD 'YOUR_READONLY_PASSWORD';
GRANT CONNECT ON DATABASE postgres TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
-- No INSERT/UPDATE/DELETE grants for readonly_user

-- Future tables should also be readable by readonly_user
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;

-- Revoke critical DDL privileges from app_user just in case (Public role usually has some)
-- In standard Postgres, 'public' might have CREATE.
REVOKE CREATE ON SCHEMA public FROM app_user;

-- Verification Query (Run this logically to check)
-- SELECT * FROM information_schema.role_table_grants WHERE grantee = 'app_user';
