-- [USAGE GUIDE]
-- 1. Replace 'YOUR_SECURE_PASSWORD' and 'YOUR_READONLY_PASSWORD' with real passwords below.
-- 2. Run the ENTIRE script at once (Top to Bottom).
--    (This script is safe to re-run; it checks if users exist before creating them.)

-- 1. Create app_user (Safe if exists)
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'app_user') THEN

      CREATE ROLE app_user LOGIN PASSWORD 'YOUR_SECURE_PASSWORD';
   END IF;
END
$do$;

-- 2. Update password if needed (Optional, uncomment to force password update)
-- ALTER USER app_user WITH PASSWORD 'YOUR_SECURE_PASSWORD';

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

-- 3. Create readonly_user (Safe if exists)
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'readonly_user') THEN

      CREATE ROLE readonly_user LOGIN PASSWORD 'YOUR_READONLY_PASSWORD';
   END IF;
END
$do$;

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
