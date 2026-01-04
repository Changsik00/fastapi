#!/bin/bash
set -e

# Usage: ./scripts/manual_migrate.sh [OPTIONAL_DB_URL]
# Automatically loads from .env if present.

# 0. Load .env file if it exists
if [ -f .env ]; then
    echo "📄 Loading configuration from .env..."
    export $(grep -v '^#' .env | xargs)
fi

TARGET_DB_URL="$1"

# 1. Resolve Target DB URL
if [ -z "$TARGET_DB_URL" ]; then
    if [ -n "$MIGRATION_DB_URL" ]; then
        TARGET_DB_URL="$MIGRATION_DB_URL"
        echo "🔹 Using MIGRATION_DB_URL from .env"
    elif [ -n "$DATABASE_URL" ]; then
        TARGET_DB_URL="$DATABASE_URL"
        echo "🔹 Using DATABASE_URL from .env"
    else
        echo "❌ Error: Could not find DB URL in arguments or .env (MIGRATION_DB_URL / DATABASE_URL)."
        exit 1
    fi
fi

# 2. Extract params for pg_dump (stripping asyncpg driver for standard postgres tool)
# This is a naive replacement for standard URLs. 
# pg_dump doesn't understand 'postgresql+asyncpg://', so we replace it with 'postgresql://'
PG_DUMP_URL="${TARGET_DB_URL//+asyncpg/}"

echo "=============================================="
echo "🛡️  Safe Manual Migration Script"
echo "Target: $TARGET_DB_URL"
echo "=============================================="

# 3. Safety Confirmation
read -p "⚠️  Are you sure you want to migrate this database? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "🚫 Migration cancelled."
    exit 1
fi

# 4. Backup (pg_dump)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_pre_migrate_$TIMESTAMP.sql"

echo "📦 Starting Backup ($BACKUP_FILE)..."
if command -v pg_dump &> /dev/null; then
    pg_dump "$PG_DUMP_URL" --no-owner --no-acl > "$BACKUP_FILE"
    echo "✅ Backup completed: $BACKUP_FILE"
else
    echo "⚠️  Warning: 'pg_dump' command not found!"
    echo "   (To fix: brew install libpq && brew link --force libpq)"
    echo "   Skipping backup..."
    
    read -p "⚠️  Proceed without backup? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "🚫 Cancelled."
        exit 1
    fi
fi

# 5. Migration (Alembic)
echo "🚀 Running Alembic Migration..."
# Temporarily set DATABASE_URL to the target for this command only
DATABASE_URL="$TARGET_DB_URL" uv run alembic upgrade head

echo "=============================================="
echo "✅ Migration Successfully Applied!"
echo "=============================================="
