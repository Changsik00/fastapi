# Tasks: Authentication (JWT) & RBAC

- [ ] **Infrastructure Layer** (Current Step) <!-- id: 1 -->
    - [x] Create `app/domain/models/user.py` with `User` and `UserRole` <!-- id: 2 -->
    - [x] Create `app/domain/repository_interfaces/user_repository.py` <!-- id: 3 -->
    - [x] Create `app/infrastructure/repositories/postgres_user_repository.py` <!-- id: 4 -->
    - [x] Add Alembic migration for `User` table <!-- id: 5 -->

- [ ] **Application Layer** <!-- id: 6 -->
    - [x] Create `app/services/auth_service.py` (Hash, JWT, Authenticate) <!-- id: 7 -->

- [ ] **Presentation Layer** (Current Step) <!-- id: 8 -->
    - [x] Add `app/api/deps.py` (get_current_user, get_current_admin) <!-- id: 9 -->
    - [x] Create `app/api/v1/endpoints/auth.py` (Login, Signup) <!-- id: 10 -->
    - [x] Register router in `app/main.py` <!-- id: 11 -->

- [ ] **Verification** (Current Step) <!-- id: 12 -->
    - [ ] Unit Test: Password Hashing & JWT <!-- id: 13 -->
    - [ ] Integration Test: Signup & Login Flow <!-- id: 14 -->
    - [ ] Integration Test: Role-Based Access (Admin vs User) <!-- id: 15 -->
