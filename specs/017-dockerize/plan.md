# Implementation Plan - Dockerize

## Goal
Create a production-ready `Dockerfile` using `uv` and deploy to Render.

## User Review Required
- [ ] **Dockerfile Strategy**: Confirm multi-stage build approach with `uv`.

## Proposed Changes

### Docker Configuration
#### [NEW] [Dockerfile](file:///Users/ck/Project/Changsik/fastapi/Dockerfile)
- Multi-stage build (builder + runner).
- `COPY pyproject.toml`, `uv.lock`.
- `RUN uv sync`.
- `COPY app/ app/`.

#### [NEW] [.dockerignore](file:///Users/ck/Project/Changsik/fastapi/.dockerignore)
- Standard Python ignore patterns.

## Verification Plan

### Automated Tests
- [ ] **Build Test**: `docker build -t fastapi-app .`
- [ ] **Run Test**: `docker run --env-file .env -p 8000:8000 fastapi-app`
- [ ] **Health Check**: `curl http://localhost:8000/health` (or `/api/v1/items`)

### Manual Verification
- [ ] **Render Deploy**: 
    1.  Push code to GitHub.
    2.  Create Web Service on Render.
    3.  Select Repository.
    4.  Set Environment Variables in Dashboard.
    5.  Verify live URL.
