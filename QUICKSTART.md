# StudyLink Quick Start Guide

A fast-track guide to get StudyLink running locally with Docker, seed sample data, and start development.

## Prerequisites

Before starting, ensure you have installed:

- **Docker** & **Docker Compose** ([Install Docker Desktop](https://www.docker.com/products/docker-desktop))
- **Git** ([Install Git](https://git-scm.com/))
- **Node.js & npm** (for frontend local development; optional if using Docker)
- **Python 3.11+** & **uv** (for backend local development; optional if using Docker)

## Option 1: Quick Start with Docker Compose (Recommended)

The fastest way to get everything running locally.

### 1. Clone and Setup Environment

```powershell
# Clone the repository
git clone <repository-url>
cd studylink

# Create .env file (if not already present)
# The project comes with sensible defaults, so you can use as-is for local development
```

### 2. Start the Stack

```powershell
# Start all services in watch mode (auto-reload on code changes)
docker compose watch
```

Wait 1-2 minutes for the stack to fully initialize. The first startup takes longer while the database sets up.

### 3. Verify Services Are Running

Open these URLs in your browser:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:5173 | React app - StudyLink UI |
| **Backend API** | http://localhost:8000 | FastAPI REST API |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |
| **Database Admin** | http://localhost:8080 | Adminer DB interface |
| **Traefik UI** | http://localhost:8090 | Proxy/routing dashboard |

### 4. Seed Sample Data

Open a **new terminal** and run:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m app.populate_sample_data
```

This populates the database with 5 sample users (see [SAMPLE_DATA_USERS.md](SAMPLE_DATA_USERS.md)):
- john.doe@example.com
- jane.smith@example.com
- bob.johnson@example.com
- alice.williams@example.com
- charlie.brown@example.com

All sample users have password: `password123`

### 5. Test the App

1. Go to http://localhost:5173
2. Sign in with any sample user (e.g., john.doe@example.com / password123)
3. Explore researchers, projects, and chat features

## Option 2: Local Development (Backend & Frontend Separately)

For active development with hot-reload and debugging.

### Backend Setup

```powershell
cd backend

# Install dependencies
uv sync

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run development server (requires running database, see docker-compose)
fastapi dev app/main.py
```

Server will be at http://localhost:8000

### Frontend Setup

```powershell
cd frontend

# Install Node version manager (if not already installed)
# Using fnm (Fast Node Manager):
# Install from: https://github.com/Schniz/fnm#installation

# Switch to correct Node version
fnm install
fnm use

# Install dependencies
npm install

# Start development server
npm run dev
```

Server will be at http://localhost:5173

### Database Setup (If Not Using Docker)

You still need a PostgreSQL database. Either:
- Keep the Docker database running: `docker compose up db`
- Or configure PostgreSQL locally and update `.env` file

## Option 3: Hybrid Approach

Run Docker services (database, etc.) but develop backend/frontend locally:

```powershell
# Terminal 1: Start only the database
docker compose up db

# Terminal 2: Backend local development
cd backend
.\.venv\Scripts\Activate.ps1
fastapi dev app/main.py

# Terminal 3: Frontend local development
cd frontend
npm run dev
```

This gives you faster iteration than full Docker while keeping infrastructure simple.

## Common Tasks

### View Logs

```powershell
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

### Stop Everything

```powershell
# Stop all running services
docker compose stop

# Stop and remove containers (keeps data)
docker compose down

# Stop and remove everything including volumes (clears database)
docker compose down -v
```

### Restart a Service

```powershell
# Useful if something breaks
docker compose restart backend
docker compose restart frontend
docker compose restart db
```

### Access Database via Admin Panel

1. Go to http://localhost:8080
2. Select **PostgreSQL**
3. Server: `db`
4. Username: see `.env` (usually `postgres`)
5. Password: see `.env`
6. Database: see `.env` (usually `app`)

### Regenerate API Client (TypeScript)

After backend API changes:

```powershell
# From project root
./scripts/generate-client.sh
```

Frontend types will auto-update from OpenAPI schema.

## Seeding Data Workflow

### Reset Database and Reseed

```powershell
# Stop services
docker compose down -v

# Start database
docker compose up db

# Seed data
cd backend
.\.venv\Scripts\Activate.ps1
python -m app.populate_sample_data
```

### View Seeded Users

See [SAMPLE_DATA_USERS.md](SAMPLE_DATA_USERS.md) for complete user details including:
- Email addresses
- Passwords
- Roles and institutions
- Linked researcher profiles

## Development Workflows

### 1. Backend API Development

```powershell
# Terminal 1: Watch mode (auto-restart on code changes)
docker compose watch

# Terminal 2 (optional): Manual testing
curl http://localhost:8000/api/v1/users/

# Or use Swagger UI at http://localhost:8000/docs
```

### 2. Frontend Component Development

```powershell
cd frontend
npm run dev

# Open http://localhost:5173 in browser
# Hot-reload on file save
```

### 3. Database Schema Changes

```powershell
cd backend
.\.venv\Scripts\Activate.ps1

# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migration
alembic upgrade head
```

## Running Tests

### Backend Tests

```powershell
cd backend
.\.venv\Scripts\Activate.ps1

# Run all tests
pytest

# Run specific test file
pytest tests/api/test_users.py

# Run with coverage
pytest --cov=app
```

### Frontend Tests

```powershell
cd frontend

# Run Playwright E2E tests
npm run test

# Run tests in UI mode
npm run test:ui
```

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing instructions.

## Troubleshooting

### Database Won't Connect

```powershell
# Check if database is healthy
docker compose ps

# View database logs
docker compose logs db

# Restart database
docker compose restart db
```

### Port Already in Use

If port 5173 (frontend), 8000 (backend), or others are in use:

```powershell
# Find and kill process using port
# On Windows, find PID:
netstat -ano | findstr :5173

# Kill process
taskkill /PID <pid> /F
```

### Docker Image Build Fails

```powershell
# Clear Docker cache and rebuild
docker compose build --no-cache

# Then start
docker compose watch
```

### Backend Virtual Environment Issues

```powershell
cd backend

# Remove old venv
Remove-Item -Recurse .venv

# Reinstall
uv sync
.\.venv\Scripts\Activate.ps1
```

### Sample Data Won't Seed

```powershell
cd backend
.\.venv\Scripts\Activate.ps1

# Check current environment
python -c "from app.core.config import settings; print(settings.database_url)"

# Verify database connection
python -c "from app.core.db import engine; engine.connect()"

# Try seeding with verbose output
python -m app.populate_sample_data
```

## Next Steps

- Read [README.md](README.md) for project overview
- Check [development.md](development.md) for detailed development info
- Review [TESTING_GUIDE.md](TESTING_GUIDE.md) for testing practices
- See [SECURITY.md](SECURITY.md) for authentication details
- Check [REALTIME_MESSAGING.md](REALTIME_MESSAGING.md) for chat/WebSocket features

## Project Structure Quick Reference

```
studylink/
├── backend/              # FastAPI REST API
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── crud/        # Database queries
│   │   ├── models/      # SQLModel ORM models
│   │   ├── schemas/     # Pydantic response schemas
│   │   └── core/        # Config, DB, security
│   └── tests/           # Backend tests
├── frontend/            # React + TypeScript + Vite
│   ├── src/
│   │   ├── routes/      # Page components
│   │   ├── components/  # Reusable UI components
│   │   └── lib/         # Utilities, API client
│   └── tests/           # E2E tests
├── scripts/             # Deployment and utility scripts
└── docker-compose.yml   # Local development stack
```

## Getting Help

- Check terminal logs: `docker compose logs -f`
- Review detailed docs in [development.md](development.md)
- Run tests to verify setup: `cd backend && pytest`
- Check existing issues and PRs in the repository
