# Implementation Plan

## Architecture
- **Location**: New module `src/app/errors/http_error_handlers.py`.
- **Registration**: Import and register in `src/app/main.py` using `app.add_exception_handler`.

## Proposed Changes

### New Files
#### [NEW] [src/app/errors/http_error_handlers.py](file:///Users/ck/Project/Changsik/fastapi/src/app/errors/http_error_handlers.py)
- Define `http_404_handler` function.
- Logic: Returns `JSONResponse` with status 404 and content `{"code": "NOT_FOUND", ...}`.

### Modified Files
#### [MODIFY] [src/app/main.py](file:///Users/ck/Project/Changsik/fastapi/src/app/main.py)
- Import `http_404_handler`.
- Add `app.add_exception_handler(404, http_404_handler)`.

## Verification Plan
### Automated Tests
- Create `tests/contract/test_errors.py`.
- Test case: `GET /non-existent-route` -> Assert JSON response matches the specified format.
