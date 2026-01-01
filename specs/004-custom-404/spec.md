# Feature Specification: Custom 404 Exception Handler

## Summary
Implement a global exception handler for `404 Not Found` errors in FastAPI. Currently, accessing undefined routes returns a default response. we want a consistent JSON structure for all 404 errors.

## Problem Statement
- Accessing `/test/` or other undefined routes returns a generic 404 response.
- We need a predictable JSON error format for client consumption.

## Requirements
- Catch `404 Not Found` errors globally.
- Return a JSON response with a standardized error structure.
- **Target Format** (Proposed):
  ```json
  {
      "code": "NOT_FOUND",
      "message": "The requested resource was not found",
      "path": "/requested/url"
  }
  ```
- Ensure Swagger UI (`/docs`) works as expected.
