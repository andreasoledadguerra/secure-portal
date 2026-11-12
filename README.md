# 🔐 Secure Portal - MFA Authentication System

A robust backend system featuring a **Multi-Factor Authentication (MFA)** flow built from scratch. Designed to protect portals with sensitive data using passwords and Time-based One-Time Passwords (TOTP).

## Key Features
- **Secure Registration**: Password hashing using `bcrypt`.
- **TOTP from Scratch**: Custom implementation of the RFC 6238 algorithm using `hmac` and `hashlib` (no third-party libraries like PyOTP).
- **Two-Factor Authentication (MFA)**: Password validation (1st factor) + 6-digit code validation (2nd factor).
- **JWT (JSON Web Tokens)**: Issuance of Access, Refresh, and Temporary (Temp) tokens for the intermediate MFA step.
- **Brute-Force Protection**: Temporary account lockout after multiple failed MFA attempts.
- **Real-Time Events**: Uses PostgreSQL `LISTEN/NOTIFY` and `asyncpg` to audit events (logins, failures, registrations).
- **Clean Architecture**: Strict separation of concerns (Routers, Services, Core, Models).
- **Fully Dockerized**: Reproducible environment with PostgreSQL and FastAPI.
- **Automated Testing**: Integration tests with `pytest` that validate the entire flow.

## Tech Stack
- **Backend**: Python 3.11, FastAPI, Uvicorn.
- **Database**: PostgreSQL 15.
- **ORM & Migrations**: SQLAlchemy 2.0 (Async), Alembic.
- **Security**: Passlib (bcrypt), Python-Jose (JWT).
- **Testing**: Pytest, HTTPX.

## How to Run the Project
1. Clone the repository and navigate into the directory:
   ```bash
   git clone <your-repository-url>
   cd secure-portal
   ```

2. Start the containers (API + Database):
    ```bash
    docker compose up -d --build
    ```

3. Apply database migrations:
    ```bash
    docker compose exec api alembic upgrade head
    ```

4. Open your broser and access the web interface
    http://localhost:8000
    
## Run Automated Tests
The project includes an integration test that simulates the complete flow (Register -> Login -> MFA -> Protected Route).

    ```bash
    docker compose exec api pytest tests/ -v
    ```
## Design Decisions and Architecture

- TOTP:  The RFC 6238 algorithm was implemented step-by-step (HMAC-SHA1, dynamic truncation) to demonstrate a deep understanding of the cryptography behind MFA.

- Token Management: A very short-lived temp_token is used, which only grants access to the MFA verification endpoint. This prevents an attacker with a compromised password from gaining full access.

- Asynchronous Listener: A dedicated asyncpg connection is used outside the SQLAlchemy ORM to listen to PostgreSQL events without blocking FastAPI's main event loop.

- Frontend: A minimalist HTML/Vanilla JS interface served by FastAPI itself to demonstrate the flow without the need for a separate Node.js server.

