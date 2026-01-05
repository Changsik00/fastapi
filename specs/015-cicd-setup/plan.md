# Plan: CI/CD Pipeline Setup

## Goal
Establish a GitHub Actions workflow to automatically lint and test the codebase.

## Proposed Changes

### 1. Workflow Configuration
#### [NEW] [.github/workflows/ci.yml](file:///Users/ck/Project/Changsik/fastapi/.github/workflows/ci.yml)
- **Name**: `CI`
- **Triggers**: `push` (branches: main), `pull_request` (branches: main)
- **Jobs**:
    - `test`:
        - `runs-on`: `ubuntu-latest`
        - `steps`:
            - Checkout code
            - Install `uv`
            - Set up Python 3.12
            - Install dependencies (`uv sync`)
            - Run Lint (`uv run ruff check .`)
            - Run Tests (`uv run pytest`)

## Verification Plan
### Automated Verification
- Push this branch to GitHub.
- Verify that the "CI" action is triggered in the "Actions" tab.
- Verify that Lint and Test steps pass successfully.

## Decisions & Issues Log
| ID | Decision | Rationale | Status |
|----|----------|-----------|--------|
| | | | |
