# Tasks: CRUD API Endpoints

**Input**: Design documents from `/specs/002-crud-api-endpoints/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included as requested in the implementation plan (TDD).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root, as defined in `plan.md`.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Ensure the basic project structure for the new feature is in place.

- [X] T001 Create domain model directory `src/domain/models/` if it doesn't exist.
- [X] T002 Create domain repository interface directory `src/domain/repositories/` if it doesn't exist.
- [X] T003 Create infrastructure repository directory `src/infrastructure/repositories/` if it doesn't exist.
- [X] T004 Create application router directory `src/app/routers/` if it doesn't exist.
- [X] T005 Create contract test directory `tests/contract/` if it doesn't exist.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define the data model and repository contract that all CRUD operations will depend on.

- [X] T006 [P] Define the `Item` and `ItemCreate` Pydantic models in `src/domain/models/item.py` based on `data-model.md` and `openapi.yml`.
- [X] T007 Define the abstract `ItemRepository` interface in `src/domain/repositories/item.py` with methods for `create`, `get_by_id`, `get_all`, `update`, and `delete`.
- [X] T008 Implement the `InMemoryItemRepository` in `src/infrastructure/repositories/in_memory_item_repository.py`, ensuring it implements the `ItemRepository` interface.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Create an Item (Priority: P1) 🎯 MVP

**Goal**: As a user, I can create a new item by providing its name and optional description.
**Independent Test**: Send a POST request to `/items/` with valid data and verify a 201 response with the new item's data and ID.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T009 [US1] Write a contract test in `tests/contract/test_items.py` for `POST /items/` to create an item and assert the response.

### Implementation for User Story 1

- [X] T010 [US1] Implement the `create` method in `InMemoryItemRepository` in `src/infrastructure/repositories/in_memory_item_repository.py`.
- [X] T011 [US1] Create the items router in `src/app/routers/items.py` and implement the `POST /items/` endpoint. Use dependency injection to provide the repository.
- [X] T012 [US1] Wire the new items router into the main FastAPI app in `src/app/main.py`.

**Checkpoint**: User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Read Items (Priority: P2)

**Goal**: As a user, I can retrieve a list of all items and retrieve a single item by its ID.
**Independent Test**: Send GET requests to `/items/` and `/items/{item_id}` and verify the responses.

### Tests for User Story 2 ⚠️

- [X] T013 [P] [US2] Write a contract test in `tests/contract/test_items.py` for `GET /items/` to retrieve all items.
- [X] T014 [P] [US2] Write a contract test in `tests/contract/test_items.py` for `GET /items/{item_id}` to retrieve a single item. Include a test for a non-existent item (404).

### Implementation for User Story 2

- [X] T015 [US2] Implement the `get_all` and `get_by_id` methods in `InMemoryItemRepository` in `src/infrastructure/repositories/in_memory_item_repository.py`.
- [X] T016 [US2] Implement the `GET /items/` and `GET /items/{item_id}` endpoints in `src/app/routers/items.py`.

**Checkpoint**: User Stories 1 and 2 should be functional.

---

## Phase 5: User Story 3 - Update an Item (Priority: P3)

**Goal**: As a user, I can update an existing item's name and description.
**Independent Test**: Create an item, then send a PUT request to `/items/{item_id}` and verify the item was updated.

### Tests for User Story 3 ⚠️

- [X] T017 [US3] Write a contract test in `tests/contract/test_items.py` for `PUT /items/{item_id}`. Include a test for updating a non-existent item (404).

### Implementation for User Story 3

- [X] T018 [US3] Implement the `update` method in `InMemoryItemRepository` in `src/infrastructure/repositories/in_memory_item_repository.py`.
- [X] T019 [US3] Implement the `PUT /items/{item_id}` endpoint in `src/app/routers/items.py`.

**Checkpoint**: User Stories 1, 2, and 3 should be functional.

---

## Phase 6: User Story 4 - Delete an Item (Priority: P4)

**Goal**: As a user, I can delete an existing item.
**Independent Test**: Create an item, send a DELETE request to `/items/{item_id}`, then verify it's gone.

### Tests for User Story 4 ⚠️

- [X] T020 [US4] Write a contract test in `tests/contract/test_items.py` for `DELETE /items/{item_id}`. Include a test for deleting a non-existent item (404).

### Implementation for User Story 4

- [X] T021 [US4] Implement the `delete` method in `InMemoryItemRepository` in `src/infrastructure/repositories/in_memory_item_repository.py`.
- [X] T022 [US4] Implement the `DELETE /items/{item_id}` endpoint in `src/app/routers/items.py`.

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup.

- [X] T023 Run all tests and ensure they pass.
- [ ] T024 Validate the implementation by running the `curl` commands in `specs/002-crud-api-endpoints/quickstart.md`.

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup. Blocks all user stories.
- **User Stories (Phases 3-6)**: Depend on Foundational. Can be implemented sequentially (P1 -> P2 -> P3 -> P4).
- **Polish (Phase 7)**: Depends on all user stories being complete.

### Within Each User Story
- Tests MUST be written and FAIL before implementation.
- Repository methods before router endpoints.
