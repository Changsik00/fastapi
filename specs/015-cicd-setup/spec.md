# Spec: CI/CD Pipeline Setup

## 1. Background
To ensure code quality and prevent regressions, we need an automated pipeline that runs linting and testing on every code change.

## 2. Requirements
- **Trigger**:
    - Push to `main` branch.
    - Pull Request to `main` branch.
- **Environment**:
    - OS: `ubuntu-latest`
    - Python: `3.12`
- **Jobs**:
    1. **Linting**: Use `ruff` to check code style and errors.
    2. **Testing**: Use `pytest` to run all tests.
- **Package Manager**: Use `uv` for fast dependency installation.

## 3. Scope
- **In Scope**: `.github/workflows/ci.yml` creation.
- **Out of Scope**: CD (Deployment) - intended for later.
