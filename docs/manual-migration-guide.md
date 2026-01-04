# Manual Migration Script Guide (`scripts/manual_migrate.sh`)

## 1. Intent (의도)
CI/CD 파이프라인이 구축되기 전 단계나, 긴급 상황에서 개발자가 로컬 머신에서 원격 데이터베이스(운영/스테이징)로 마이그레이션을 안전하게 수행하기 위해 제작되었습니다.

**"Safe Safety Net"**
단순히 `alembic upgrade`를 실행하는 것이 아니라, **자동 백업**과 **이중 확인** 절차를 강제하여 실수로 인한 데이터 손실을 방지합니다.

## 2. Usage (사용법)

### Prerequisites (전제 조건)
*   **Target Database**: 접속 가능한 원격 DB 주소.
*   **`pg_dump`**: PostgreSQL 백업 도구 (설치: `brew install libpq && brew link --force libpq`).
*   **`.env`**: 프로젝트 루트에 `.env` 파일 존재 (권장).

### Execution (실행)
프로젝트 루트에서 다음 명령어를 실행합니다.

```bash
# Method A: .env 파일의 설정을 자동으로 읽어와 실행 (추천)
./scripts/manual_migrate.sh

# Method B: 직접 DB URL을 인자로 주입하여 실행
./scripts/manual_migrate.sh "postgresql+asyncpg://user:pass@host:5432/dbname"
```

## 3. Workflow (작동 원리)
1.  **Config Load**: `.env` 파일에서 `MIGRATION_DB_URL` (1순위) 또는 `DATABASE_URL` (2순위)을 읽어옵니다.
2.  **Safety Check**: 대상 DB URL을 보여주고, 정말 진행할지 `y/N`으로 물어봅니다.
3.  **Auto Backup**: `pg_dump`를 사용하여 현재 DB 상태를 `backup_pre_migrate_YYYYMMDD_HHMMSS.sql` 파일로 스냅샷 저장합니다.
    *   `pg_dump`가 없으면 경고 후 중단하거나 사용자 동의 하에 백업 없이 진행합니다.
4.  **Execute**: `uv run alembic upgrade head`를 실행하여 스키마를 변경합니다.

## 4. Precautions (주의 사항)
*   **Backup File**: 생성된 `.sql` 백업 파일은 `.gitignore`에 포함되어 있지 않을 수 있으니, **절대 Git에 커밋하지 마세요.** (민감한 데이터 포함 가능성)
*   **Production**: 실제 운영 DB에 수행할 때는 반드시 팀 공유 후 진행하세요.
*   **Connection**: 반드시 Port 5432 (Session Mode)로 연결해야 안정적입니다. (Supabase Transaction Mode 6543 사용 지양)
