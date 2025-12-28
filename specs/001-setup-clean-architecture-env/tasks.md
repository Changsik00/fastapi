# Tasks: FastAPI Clean Architecture Environment Setup

**Input**: Design documents from `/specs/001-setup-clean-architecture-env/`
**Prerequisites**: plan.md, spec.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [X] T001 Create Clean Architecture project structure (`src/app`, `src/core`, `src/domain`, `src/infrastructure`)
- [X] T002 Create test directory structure (`tests/contract`, `tests/integration`, `tests/unit`)
- [X] T003 Create Python virtual environment using `uv venv`
- [X] T004 Install `fastapi` and `uvicorn` into the virtual environment using `uv pip install fastapi uvicorn`
- [X] T005 Generate `requirements.txt` file using `uv pip freeze > requirements.txt`

---

## Phase 2: User Story 1 - "Hello World" API Endpoint (Priority: P2) 🎯 MVP

**Goal**: Provide a working "Hello World" endpoint to verify the basic application setup.

**Independent Test**: The endpoint can be tested with a `curl` command or an automated test.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T006 [P] [US1] Create contract test `tests/contract/test_main.py` that sends a GET request to `/` and asserts a 200 status code and the expected JSON response.

### Implementation for User Story 1

- [X] T007 [US1] Create `src/app/main.py` with a FastAPI app instance and a `GET /` endpoint that returns `{"message": "Hello World"}`.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must be completed before anything else.
- **Phase 2 (User Story 1)** depends on the completion of Phase 1.
- Within User Story 1, the test (T006) should be written before the implementation (T007).
