# Feature Specification: Fix Existing Tests & Pydantic Warnings

## Summary
The current codebase fails `uv run pytest` due to an assertion error in `test_read_main` and emits multiple Pydantic v2 deprecation warnings. We need to fix the tests to be green and resolve the warnings for a clean build.

## Problem Statement
1. **Assertion Error**: `test_read_main` expects `{"message": "Hello World"}` but the API returns `{"message": "Welcome to the Clean Architecture example!"}`.
2. **Deprecation Warnings**: Code uses Pydantic V1 syntax (e.g., `orm_mode`, `.dict()`, `class Config`).

## Requirements
- Update `test_read_main` to match the actual API response (or update API to match test - assumption: API is correct).
- Update Pydantic models to V2 syntax.
    - `orm_mode` -> `from_attributes`
    - `class Config` -> `model_config = ConfigDict(...)`
    - `.dict()` -> `.model_dump()`
- **Goal**: `uv run pytest` passes with 0 failures and 0 warnings.
