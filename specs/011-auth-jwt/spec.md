# Specification: Authentication (JWT)

## 1. Background
Currently, the API has no user authentication. Anyone can access all endpoints. To build a secure production-ready service, we need to implement a user login system using JWT (JSON Web Tokens).

## 2. Requirements
- **User Domain**: Create a `User` entity with email, password_hash, and **`role`**.
- **Role-Based Access Control (RBAC)**: Support `admin` (full access) and `user` (or `readonly`) roles.
- **Registration**: Endpoint to create a new user (default role: `user`).
- **Login**: Endpoint to authenticate user and return an Access Token (JWT).
- **Protection**: Secure endpoints to require valid JWT. Admin-only routes.
- **Crypto**: Use `bcrypt` (or `argon2`) for password hashing.
- **Algorithm**: HS256 for JWT signing (keep it simple for now).

## 3. User Stories
- As a **User**, I want to sign up with my email and password.
- As a **User**, I want to log in and get a token so I can access protected resources.
- As a **System**, I want to reject requests with invalid tokens to protect data.

## 4. Constraints
- **Library**: Use `python-jose` or `pyjwt` and `passlib[bcrypt]`.
- **DB**: Use `SQLModel` for the User table.
- **Arch**: Follow Clean Architecture (User Entity, Repository, Service at Use Case layer).
