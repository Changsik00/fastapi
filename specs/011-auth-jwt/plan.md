# Plan: Authentication (JWT)

## Goal
Implement a secure user authentication system using JWT (JSON Web Tokens) to protect API endpoints.

## User Review Required
> [!IMPORTANT]
> **Library Choice**: We will use `passlib[bcrypt]` for strict password hashing and `python-jose` for JWT handling.
> **Database**: A new `User` table will be created. Migration is required.

## Proposed Changes

### Domain Layer (Business Rules)
#### [NEW] [app/domain/models/user.py](file:///Users/ck/Project/Changsik/fastapi/app/domain/models/user.py)
- `User` SQLModel (id, email, password_hash, is_active, **role**).
- `UserRole` Enum (`ADMIN`, `USER`).

#### [NEW] [app/domain/repository_interfaces/user_repository.py](file:///Users/ck/Project/Changsik/fastapi/app/domain/repository_interfaces/user_repository.py)
- Interface for user persistence (`get_by_email`, `create`, `get_multi`).
- `get_multi(skip, limit, role)` for filtered list.

### Infrastructure Layer (Persistence)
#### [NEW] [app/infrastructure/repositories/postgres_user_repository.py](file:///Users/ck/Project/Changsik/fastapi/app/infrastructure/repositories/postgres_user_repository.py)
- Concrete implementation using `AsyncSession`.

### Application Layer (Use Cases)
#### [NEW] [app/services/auth_service.py](file:///Users/ck/Project/Changsik/fastapi/app/services/auth_service.py)
- `authenticate_user(email, password)`
- `create_access_token(data)`
- `get_password_hash(password)`

### Presentation Layer (API)
#### [NEW] [app/api/v1/endpoints/auth.py](file:///Users/ck/Project/Changsik/fastapi/app/api/v1/endpoints/auth.py)
- `POST /auth/login`: Returns JWT token.
- `POST /auth/signup`: Registers new user.

#### [MODIFY] [app/api/deps.py](file:///Users/ck/Project/Changsik/fastapi/app/api/deps.py)
- Add `get_current_user` dependency to protect routes.

## Verification Plan

### Automated Tests
- **Unit Tests**: Test password hashing and token generation.
- **Integration Tests**:
    - `POST /auth/signup` -> 200 OK
    - `POST /auth/login` -> 200 OK and returns `access_token`
    - `GET /protected-route` (without token) -> 401 Unauthorized
    - `GET /protected-route` (with token) -> 200 OK
