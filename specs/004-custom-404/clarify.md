# Clarification & Research

## Questions
- **Q**: What should the error response looks like?
    - **A**: Proposed: `{"code": "NOT_FOUND", "message": "...", "path": "..."}`. This provides more context than just "Not Found".
- **Q**: Should this apply to API routes only or all routes?
    - **A**: Since this is an API-first project, it should apply globally to the FastAPI app.

## Constraints
- Must not break the existing Swagger UI (`/docs`) or ReDoc (`/redoc`).
- Must utilize FastAPI's `exception_handler` mechanism.
