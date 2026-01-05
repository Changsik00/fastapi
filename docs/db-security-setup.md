# 데이터베이스 보안 설정 가이드 (Role Separation)

## 개요 (Overview)
이 가이드는 **역할 분리(Role Separation)**를 통해 Supabase/PostgreSQL 데이터베이스의 보안을 강화하는 방법을 설명합니다.
이 설정은 애플리케이션이 실수로 테이블을 삭제하거나 스키마를 변경하는 것을 방지합니다.

## 역할 (Roles) 정의

**현재 상황**: `.env`에 있는 정보는 **관리자(Admin/Superuser)** 계정입니다.
(`postgres[.project_ref]` 등). 이 계정은 모든 권한이 있어 위험합니다.

우리의 목표는 **새로운, 힘이 약한 계정**을 하나 더 만드는 것입니다.

1.  **Migration User (기존 계정)**
    -   **계정명**: `postgres` (또는 `.env`에 있는 현재 사용자)
    -   **비밀번호**: 현재 `.env`에 있는 비밀번호 (`pmqj...`)
    -   **권한**: **신(God)**. 테이블 삭제, 생성 등 모든 것이 가능.
    -   **용도**: 앞으로는 **배포(Migration)** 때만 사용합니다.

2.  **Application User (새로 만들 계정)**
    -   **계정명**: `app_user` (스크립트로 생성)
    -   **비밀번호**: **새로 설정할 비밀번호** (스크립트에서 `YOUR_SECURE_PASSWORD` 부분을 수정)
    -   **권한**: **일반인**. 데이터 조회/추가만 가능. (테이블 삭제 불가)
    -   **용도**: **FastAPI 서버**가 평소에 사용합니다.

3.  **Read-Only User (협업용 계정)**
    -   **계정명**: `readonly_user`
    -   **비밀번호**: **팀원 공유용 비밀번호** (`YOUR_READONLY_PASSWORD` 수정)
    -   **권한**: **구경꾼**. 데이터 **조회(SELECT)**만 가능.
    -   **용도**: 개발자나 데이터 분석가가 DB 내용을 확인하고 싶을 때 사용. (실수 방지)

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
