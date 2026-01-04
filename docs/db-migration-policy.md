# Database Migration Safety Policy

## 1. Golden Rule
**"운영 DB(Production Database)는 절대 사람의 손으로 직접 마이그레이션 하지 않는다."**

## 2. Workflow by Stage
### A. Local Development (Dev)
- **행위자**: 개발자 (User/Agent)
- **방법**: `alembic revision` 생성 후 `alembic upgrade head` 수동 실행.
- **목적**: 기능 개발 및 스키마 변경 검증.

### B. Pull Request (CI)
- **행위자**: GitHub Actions (CI)
- **방법**:
    1. 새 DB 컨테이너 띄움.
    2. `alembic upgrade head` 실행 (성공 여부 확인).
    3. `alembic downgrade base` (롤백 테스트, 선택사항).
- **목적**: 마이그레이션 스크립트 오타 및 로직 오류 사전 차단.

### C. Deployment (CD)
- **행위자**: 배포 스크립트 (CD)
- **시점**: **PR Merge 직후** (또는 배포 파이프라인 트리거 시).
- **순서**:
    1. **Backup**: `pg_dump`로 전체 데이터 백업.
    2. **Migrate**: `alembic upgrade head` 실행.
    3. **Deploy**: 새로운 애플리케이션 컨테이너 시작.
- **목적**: 코드와 DB 스키마의 동기화 보장.

## 3. Backward Compatibility (하위 호환성)
**Zero Downtime**을 위해 스키마 변경은 항상 하위 호환성을 유지해야 합니다.
- **예시**: 컬럼 삭제 시
    1. `v1`: 컬럼을 `nullable`로 변경 (코드에서 사용 중지).
    2. `v2`: 실제 컬럼 삭제 마이그레이션 실행.

## 4. CI/CD Security Strategy (Supabase/Postgres)
**"권한 분리(Role Separation)"** 를 통해 물리적인 안전 장치를 마련합니다.

### A. Role 구성
1.  **`migration_user` (for GitHub Actions)**
    *   **권한**: `DDL` (Create, Alter, Drop Table) + `DML`.
    *   **사용처**: GitHub Actions `SECRET`에만 저장 (`MIGRATION_DB_URL`).
    *   **목적**: 오직 CI/CD 파이프라인만이 스키마를 변경할 수 있음.

2.  **`app_user` (for FastAPI Server)**
    *   **권한**: `DML` (Select, Insert, Update, Delete) **ONLY**.
    *   **제약**: `CREATE`, `DROP` 등 DDL 권한 **Revoke** (박탈).
    *   **사용처**: 운영 서버 환경변수 (`DATABASE_URL`).
    *   **효과**: 서버 코드가 해킹당하거나 오작동해도 테이블을 날릴 수 없음.

### B. Supabase 적용 팁
*   Supabase SQL Editor에서 위 유저들을 직접 생성(`CREATE ROLE`)하여 관리합니다.
*   **Connection Pooling**: 마이그레이션(`alembic`)은 반드시 **Session Mode (Port 5432)** 로 연결해야 합니다. (Transaction Mode인 6543 포트는 DDL 트랜잭션 오류 가능성 있음).

## 5. Developer Manual Execution (Emergency/Dev Mode)
개발 편의성 및 긴급 대응을 위해 **CLI에서 수동 실행**도 가능해야 합니다.

### A. 권한 제어 방법 (How to restrict)
**"환경 변수(`DATABASE_URL`)가 곧 ID 카드입니다."**
*   **권한 부여**: 특정 개발자(팀장, 시니어)에게만 `migration_user`의 정보를 공유합니다. (1Password/Vault 등 보안 채널 이용)
*   **일반 개발자**: 로컬 Docker DB는 본인이 마스터이므로 자유롭게, 공용 Dev/Staging DB는 `app_user` (DDL 불가) 정보만 `.env`에 설정하여 지급합니다.

### B. 실행 가이드
CLI에서 `alembic` 명령어는 현재 쉘의 환경 변수(또는 `.env`)를 바라봅니다.

```bash
# 1. 권한 확인 (본인의 .env가 migration 권한이 있는 URL인지 확인)
# 예: postgresql+asyncpg://migration_user:secret@...
grep DATABASE_URL .env

# 2. 실행 (로컬에서 원격 DB로 쏨)
uv run alembic upgrade head
```
