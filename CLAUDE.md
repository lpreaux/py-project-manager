# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI project manager application built with Python, using SQLModel/SQLAlchemy for ORM and SQLite for data persistence. The application follows a layered architecture pattern with routers, services, and repositories.

## Development Setup

### Environment Setup
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Configure `.env` file with:
- `DB_NAME`: Database name (defaults to "project-manager" for SQLite)
- Note: MySQL connection variables (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT) are available in database.py but currently commented out

### Running the Application
```bash
# Start the FastAPI server
uvicorn src.main:app --reload

# The server will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Testing
```bash
# Run tests with pytest
pytest

# Run specific test file
pytest test/<test_file>.py
```

## Architecture

### Layered Architecture Pattern
The application follows a clean three-layer architecture:

1. **Routers** (`src/routers/`): Handle HTTP requests/responses and route definitions
   - Define API endpoints and request/response models
   - Create database sessions
   - Delegate business logic to services
   - Example: `user_router.py` defines `/api/v1/users` endpoints

2. **Services** (`src/servcies/`): Business logic layer (note: typo in directory name)
   - Orchestrate operations between routers and repositories
   - Contain business rules and validation
   - Instantiate and use repositories
   - Example: `UserService` manages user-related business logic

3. **Repositories** (`src/repositories/`): Data access layer
   - Handle direct database operations
   - Execute SQLModel queries
   - Accept `Session` objects as parameters
   - Example: `UserRepository` performs CRUD operations on User model

### Database Architecture
- **Engine Creation**: `database.py` creates SQLModel engine with retry logic (10 attempts, 3s delay)
- **Connection String**: Currently uses SQLite (`sqlite:///{DB_NAME}.db`), MySQL support commented out
- **Session Management**: Sessions created per-request in routers using context managers
- **Table Creation**: `create_db_and_tables()` called on app startup in `main.py`

### Router Registration Flow
1. Feature-specific routers (e.g., `user_router`) define endpoints with prefix `/users`
2. Main API router (`routers/__init__.py`) aggregates feature routers with prefix `/api/v1`
3. FastAPI app (`main.py`) includes the main router, resulting in paths like `/api/v1/users`

### Data Models
- Located in `src/models/`
- Use SQLModel (Pydantic + SQLAlchemy) for both ORM and validation
- Define `table=True` for database tables
- Example: `User` model has id, username, email, password fields

## Key Implementation Patterns

### Service Layer Pattern
Services instantiate their own repositories and accept database sessions from routers:
```python
class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self, db: Session):
        return self.repository.get_all_users(db)
```

### Session Management
Database sessions are created per-request using context managers:
```python
@router.get("/")
async def read_users():
    with Session(engine) as session:
        return service.get_all_users(session)
```

### Environment Configuration
The app uses `python-dotenv` loaded at the top of `main.py` before other imports to ensure environment variables are available throughout the application.

## Project Structure Notes

- Directory naming: `src/servcies/` has a typo (should be "services")
- Tests directory (`test/`) currently only contains `__init__.py`
- Database file is created at project root as `project-manager.db`
- All application code is under `src/` package