-- DB Role Separation Script (Supabase/PostgreSQL)
-- This script creates two roles:
-- 1. migration_user: Has full DDL privileges (for CI/CD and Alembic).
-- 2. app_user: Has DML privileges only (for the running application).

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

-- Revoke critical DDL privileges from app_user just in case (Public role usually has some)
-- In standard Postgres, 'public' might have CREATE.
REVOKE CREATE ON SCHEMA public FROM app_user;

-- Verification Query (Run this logically to check)
-- SELECT * FROM information_schema.role_table_grants WHERE grantee = 'app_user';
