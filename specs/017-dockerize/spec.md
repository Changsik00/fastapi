# Dockerize Specification

## 1. Objective
Containerize the FastAPI application using Docker.
Ensure the image is lightweight, secure, and ready for deployment on platforms like Render or Fly.io.
Use `uv` for fast and efficient dependency installation.

## 2. Requirements

### A. Dockerfile
- **Base Image**: `python:3.12-slim-bookworm` (Official, Small).
- **Builder Pattern**: Use multi-stage build to keep the final image small.
    1.  `builder`: Install `uv` and dependencies.
    2.  `runner`: Copy only the virtual environment and app code.
- **Package Manager**: `uv`.
    -   Use `uv sync --frozen --no-install-project` to install dependencies.
- **Port**: Expose `8000`.
- **Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

### B. Ignore Files
- `.dockerignore`: Exclude `__pycache__`, `.git`, `.venv` (local), `tests`, `specs`, `docs` to reduce build context size.

### C. Local Verification
- Capability to build and run the container locally.
- Connection to Supabase (Remote) should work if `.env` or env vars are passed.

## 3. Deployment (Render)
- Deploy the Docker image to Render as a Web Service.
- Configure environment variables in Render Dashboard (`DATABASE_URL`, `SECRET_KEY`).

## 4. Scope (Out of Scope)
- `docker-compose.yml` for local DB (Deferred for now, focusing on Deployment first as per user discussion).
- `render.yaml` (Deferred, manual setup first).
