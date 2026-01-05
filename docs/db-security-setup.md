# 데이터베이스 보안 설정 가이드 (Role Separation)

## 개요 (Overview)
이 가이드는 **역할 분리(Role Separation)**를 통해 Supabase/PostgreSQL 데이터베이스의 보안을 강화하는 방법을 설명합니다.
이 설정은 애플리케이션이 실수로 테이블을 삭제하거나 스키마를 변경하는 것을 방지합니다.

## 역할 (Roles)
1.  **Migration User** (`postgres` 또는 `migration_user`)
    -   **권한**: 전체 관리자 권한 (DDL + DML).
    -   **용도**: CI/CD 파이프라인, Alembic 마이그레이션, 초기 설정.
2.  **Application User** (`app_user`)
    -   **권한**: 읽기/쓰기 (DML) 전용. (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
    -   **용도**: 실행 중인 FastAPI 애플리케이션.

## 🚀 설정 방법 (Setup Instructions)

### 1. 역할 생성 스크립트 실행
1.  **Supabase Dashboard** -> **SQL Editor**를 엽니다.
2.  이 프로젝트의 `scripts/init_roles.sql` 파일 내용을 복사합니다.
3.  **중요**: 스크립트 내의 `'YOUR_SECURE_PASSWORD'`를 실제 강력한 비밀번호로 변경합니다.
4.  스크립트를 실행(Run)합니다.

### 2. 로컬 환경 설정 (`.env`)
애플리케이션이 `app_user`를 사용하도록 `.env` 파일을 업데이트합니다:
```ini
# For Application (DML) - 평소 실행용
DATABASE_URL=postgresql+asyncpg://app_user:새_비밀번호@db.xxx.supabase.co:5432/postgres

# For Migrations - 마이그레이션 실행용 (필요 시 별도 변수 관리)
# 로컬에서 마이그레이션 수행 시에는 기존 관리자 계정 정보를 사용하거나,
# MIGRATION_DB_URL 등을 별도로 정의하여 사용할 수 있습니다.
```

### 3. 프로덕션 설정 (CI/CD)
1.  GitHub Repository **Settings** -> **Secrets and variables** -> **Actions**로 이동합니다.
2.  `DATABASE_URL`이 통합 테스트 등에 사용된다면 적절한 권한의 유저인지 확인합니다.
3.  `MIGRATION_DB_URL` 시크릿이 있다면, 반드시 **관리자(Admin)** 권한(`postgres`)을 사용하도록 설정해야 합니다.

## 검증 (Verification)
설정이 올바른지 확인하기 위해 `app_user`로 접속하여 파괴적인 명령을 실행해 봅니다:
```sql
-- Connect as app_user
DROP TABLE items;
-- 결과: ERROR: permission denied for schema public
```
