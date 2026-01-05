# Tasks: Password Management

- [x] **Design & Approval** (Done) <!-- id: 1 -->
    - [x] Create Branch `014-password-mgmt` <!-- id: 2 -->
    - [x] Draft `spec.md` <!-- id: 3 -->
    - [x] Draft `plan.md` (Done) <!-- id: 4 -->

- [x] **Implementation** (Done) <!-- id: 5 -->
    - [x] **Domain**: Add DTOs (`PasswordChangeRequest` etc.) in `user.py` <!-- id: 6 -->
    - [x] **Service**: Add `change_password`, `reset_password`, `create_reset_token` to `AuthService` <!-- id: 7 -->
    - [x] **API**: Add endpoints to `auth.py` <!-- id: 8 -->

- [x] **Verification** (Done) <!-- id: 9 -->
    - [x] Create `tests/contract/test_password_mgmt.py` <!-- id: 10 -->
    - [x] Run Tests (`uv run pytest tests/contract/test_password_mgmt.py`) <!-- id: 11 -->
