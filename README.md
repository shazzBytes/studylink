# StudyLink

StudyLink is a full-stack research collaboration platform built on FastAPI, PostgreSQL, React, and TypeScript. It helps users discover researchers, browse publications, manage research projects, and communicate through a built-in chat system. This README is written as a detailed project reference so it can double as source material for a black book, viva, report, or project documentation bundle.

## 1. Project Overview

### 1.1 Problem Statement

Research students and academic collaborators often use disconnected tools for:

- researcher discovery
- publication browsing
- project coordination
- team communication

StudyLink brings these activities into one platform. A user can create an account, build a researcher profile, search for researchers and publications, create or join projects, and collaborate through chat.

### 1.2 Core Objective

The main objective of StudyLink is to provide a centralized collaboration environment for academic and research-oriented users.

### 1.3 Main User Capabilities

- Register and log in securely
- Maintain a personal user account
- Create and update a researcher profile
- Browse researchers and their publications
- Search researchers, publications, and projects
- Create public or private projects
- Add and remove project members
- Exchange messages in real time through chats
- Recover passwords using email-based reset flow

## 2. Technology Stack

### 2.1 Backend

- FastAPI for REST API development
- SQLModel for ORM and schema modeling
- PostgreSQL as the relational database
- Alembic for database migrations
- Pydantic and `pydantic-settings` for validation and configuration
- JWT authentication for protected endpoints
- Sentry integration for error monitoring outside local mode

### 2.2 Frontend

- React 19
- TypeScript
- Vite
- TanStack Router for route-based navigation
- TanStack Query for API state and caching
- React Hook Form with Zod validation
- Tailwind CSS 4
- Radix UI primitives and shadcn-style UI components
- Chakra UI is also present in dependencies, although the current UI mostly uses Tailwind/Radix-style components

### 2.3 DevOps and Tooling

- Docker Compose for local and production-style orchestration
- Nginx for frontend serving
- Traefik for reverse proxy and HTTPS-oriented deployment flow
- Playwright for frontend end-to-end tests
- Pytest for backend tests
- Biome for frontend linting
- `uv` for Python dependency management

## 3. High-Level Architecture

StudyLink follows a standard client-server architecture:

1. The React frontend provides the user interface.
2. The FastAPI backend exposes REST endpoints under `/api/v1`.
3. PostgreSQL stores users, researchers, publications, projects, memberships, chats, and messages.
4. The frontend consumes backend endpoints using a generated OpenAPI client plus a few handwritten client helpers.
5. Real-time chat updates are delivered through WebSockets.

### 3.1 Request Flow

- The frontend sends login credentials to `/api/v1/login/access-token`.
- The backend returns a JWT access token.
- The token is stored in browser local storage.
- Subsequent authenticated requests include `Authorization: Bearer <token>`.
- For chat updates, the frontend opens a WebSocket connection to the chat endpoint with the token as a query parameter.

## 4. Project Structure

```text
studylink/
├── backend/
│   ├── app/
│   │   ├── api/              # API routers and dependencies
│   │   ├── core/             # config, security, database setup
│   │   ├── crud/             # database access and business logic
│   │   ├── models/           # SQLModel database models
│   │   ├── realtime/         # chat event broadcasting
│   │   ├── schemas/          # request/response schemas
│   │   ├── alembic/          # migration versions
│   │   ├── email-templates/  # password reset and account emails
│   │   ├── initial_data.py   # DB initialization entrypoint
│   │   ├── populate_sample_data.py
│   │   └── main.py           # FastAPI app entrypoint
│   ├── tests/                # backend tests
│   ├── scripts/              # backend scripts
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── client/           # generated and custom API clients
│   │   ├── components/       # UI components
│   │   ├── hooks/            # auth and utility hooks
│   │   ├── routes/           # TanStack Router pages
│   │   ├── lib/              # demo and helper data
│   │   └── main.tsx
│   ├── tests/                # Playwright tests
│   └── package.json
├── docker-compose.yml
├── development.md
├── deployment.md
├── REALTIME_MESSAGING.md
└── README.md
```

## 5. Backend Design

### 5.1 Application Entry

The backend app starts from `backend/app/main.py`.

Responsibilities:

- creates the FastAPI app
- loads settings from the root `.env`
- registers the API router under `/api/v1`
- configures CORS
- initializes the chat event loop during startup
- enables Sentry in non-local environments when configured

### 5.2 Configuration

Configuration is handled in `backend/app/core/config.py`.

Important settings include:

- `PROJECT_NAME`
- `API_V1_STR`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `FRONTEND_HOST`
- `ENVIRONMENT`
- `BACKEND_CORS_ORIGINS`
- `POSTGRES_SERVER`
- `POSTGRES_PORT`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `POSTGRES_TEST_DB`
- `FIRST_SUPERUSER`
- `FIRST_SUPERUSER_PASSWORD`
- `SMTP_*`
- `EMAILS_FROM_EMAIL`
- `SENTRY_DSN`

### 5.3 Database Initialization

`backend/app/core/db.py` creates the SQLAlchemy/SQLModel engine and seeds demo data through `init_db(session)`.

The database initializer:

- ensures the first superuser exists
- creates demo users
- creates demo researcher profiles
- creates demo publications
- creates demo projects and project memberships
- creates demo chats and demo messages

This is important for project presentation because the system is seeded with believable content instead of being empty after setup.

## 6. Main Data Models

### 6.1 User

Defined in `backend/app/models/users.py`.

Fields:

- `id`
- `email`
- `hashed_password`
- `full_name`
- `is_active`
- `is_superuser`

Purpose:

- stores authentication and account-level information
- acts as owner of items and chats
- acts as owner or member in projects

### 6.2 ResearcherInfo

Defined in `backend/app/models/researcher.py`.

Fields:

- `id`
- `full_name`
- `email`
- `qualification`
- `institute`
- `bio`
- `is_deleted`
- `deleted_at`

Purpose:

- represents the public-facing researcher profile
- links to publications
- supports search by name, email, institute, and qualification

### 6.3 Publication

Defined in `backend/app/models/publication.py`.

Fields:

- `id`
- `researcher_id`
- `title`
- `publisher`
- `year`
- `description`
- `domains`
- `is_deleted`
- `deleted_at`

Purpose:

- stores publication metadata for a researcher
- supports publication discovery and domain-based filtering

### 6.4 Project

Defined in `backend/app/models/project.py`.

Fields:

- `id`
- `title`
- `description`
- `domain`
- `owner_id`
- `is_public`
- `is_deleted`
- `deleted_at`
- `created_at`
- `updated_at`

Purpose:

- stores research project information
- supports ownership, privacy, and collaboration

### 6.5 ProjectMember

Defined in `backend/app/models/project_member.py`.

Purpose:

- maps users to projects
- stores role-based membership such as viewer/editor

### 6.6 Chat

Defined in `backend/app/models/chat.py`.

Fields:

- `id`
- `user_id`
- `chat_type`
- `title`
- `participants`
- `member_states`
- `reported_by`
- `last_message`
- `created_at`
- `updated_at`
- `is_deleted`

Purpose:

- supports direct and group chat
- stores participants in JSON format
- tracks conversation state and moderation-related reporting

### 6.7 Message

Defined in `backend/app/models/message.py`.

Fields:

- `id`
- `chat_id`
- `sender_id`
- `content`
- `attachments`
- `created_at`
- `updated_at`
- `is_deleted`

Purpose:

- stores messages within a chat
- supports soft deletion
- stores attachment references as a JSON list

## 7. Backend Modules and Responsibilities

### 7.1 `api/`

Contains route definitions.

Major routers:

- `login.py` for token login and password recovery
- `users.py` for user CRUD and self-service account operations
- `researcher.py` for researcher profiles and publications
- `project.py` for project CRUD and project membership
- `chats.py` for chat creation, listing, update, leave, report, and chat WebSocket
- `messages.py` for per-chat message CRUD
- `search.py` for search endpoints
- `private.py` for local-development-only routes
- `utils.py` for health-check style utilities

### 7.2 `crud/`

Contains business logic and database operations separated from route handlers.

Examples:

- `project.py` handles project creation, update, soft delete, and membership checks
- `research_search.py`, `publication_search.py`, and `project_search.py` handle filtered search queries
- `chats.py` and `messages.py` handle chat and message persistence

### 7.3 `schemas/`

Contains request and response models exposed by the API.

Examples:

- `ProjectCreate`, `ProjectUpdate`, `ProjectPublic`
- `CreateChat`, `UpdateChat`, `ChatPublic`
- `MessageCreate`, `MessageUpdate`, `MessagePublic`

### 7.4 `realtime/`

Contains chat event broadcasting logic.

The current realtime implementation uses:

- backend WebSocket endpoint for authenticated connections
- in-memory connection tracking
- broadcast events such as `chat.created`, `chat.updated`, `chat.deleted`, `chat.left`, and `message.created`

## 8. API Summary

Base URL: `/api/v1`

### 8.1 Authentication

- `POST /login/access-token` -> login and receive JWT
- `POST /login/test-token` -> validate current token
- `POST /password-recovery/{email}` -> start password reset
- `POST /reset-password/` -> complete password reset

### 8.2 Users

- `POST /users/signup` -> register a new user
- `GET /users/me` -> fetch current user
- `PATCH /users/me` -> update current user profile fields
- `PATCH /users/me/password` -> change password
- `DELETE /users/me` -> delete current account
- `GET /users/` -> admin-only user listing
- `POST /users/` -> admin-only create user
- `PATCH /users/{user_id}` -> admin-only update user
- `DELETE /users/{user_id}` -> admin-only delete user

### 8.3 Researchers

- `GET /researchers/me`
- `POST /researchers/me`
- `PUT /researchers/me`
- `GET /researchers/search`
- `GET /researchers/{researcher_id}`
- `GET /researchers/{researcher_id}/publications`
- `PUT /researchers/{researcher_id}/publications`

### 8.4 Search

- `GET /search/researchers`
- `GET /search/publications`
- `GET /search/projects`

### 8.5 Projects

- `GET /projects`
- `POST /projects`
- `GET /projects/{project_id}`
- `PATCH /projects/{project_id}`
- `DELETE /projects/{project_id}`
- `GET /projects/{project_id}/members`
- `POST /projects/{project_id}/members`
- `DELETE /projects/{project_id}/members/{user_id}`

### 8.6 Chats and Messages

- `GET /chats`
- `POST /chats`
- `GET /chats/{chat_id}`
- `PATCH /chats/{chat_id}`
- `DELETE /chats/{chat_id}`
- `POST /chats/{chat_id}/leave`
- `POST /chats/{chat_id}/report`
- `GET /chats/contacts`
- `GET /chats/{chat_id}/messages`
- `POST /chats/{chat_id}/messages`
- `GET /chats/{chat_id}/messages/{message_id}`
- `PATCH /chats/{chat_id}/messages/{message_id}`
- `DELETE /chats/{chat_id}/messages/{message_id}`

### 8.7 WebSocket

- `WS /api/v1/chats/ws?token=<jwt>`

Used for realtime chat synchronization on the frontend.

## 9. Frontend Design

### 9.1 Frontend Entry and Routing

The frontend is built with TanStack Router. Main pages include:

- `/login`
- `/signup`
- `/recover-password`
- `/reset-password`
- `/`
- `/search`
- `/researchers`
- `/researchers/$id`
- `/projects`
- `/projects/create`
- `/projects/$id`
- `/chats`
- `/items`
- `/messages`
- `/notifications`
- `/profile`
- `/settings`
- `/admin`

### 9.2 Main Functional Screens

#### Dashboard

The home page currently shows a research paper feed using dummy paper data. This gives the application a discoverability-focused landing area.

#### Search

The search page:

- fetches researchers from the backend
- loads their publications
- derives research interests from publication domains
- filters researchers by text search and interest badges

#### Researchers

The `/researchers` route currently reuses the search page UI, making researcher discovery central to the product flow.

#### Projects

Projects support:

- project list view
- project creation form
- project detail page
- membership display
- owner-only delete control

#### Chats

The chats page is one of the strongest project-specific modules. It supports:

- chat listing
- contact lookup
- new chat creation
- message history
- real-time updates through WebSockets
- delete, leave, and report actions
- responsive two-pane layout

### 9.3 Frontend State Management

- TanStack Query is used for server state and cache invalidation
- route-driven navigation is handled through TanStack Router
- JWT token is stored in local storage
- current user state is fetched through `useAuth`

## 10. Authentication and Security

StudyLink uses JWT-based authentication.

Security features already implemented:

- password hashing in backend security utilities
- bearer token protection for authenticated routes
- superuser-protected admin routes
- CORS configuration through environment settings
- soft delete behavior in several entities
- password recovery flow using email templates

Important production note:

- default placeholder secrets such as `changethis` must be replaced before deployment

## 11. Seeded Demo Data

The project contains meaningful demo records in `backend/app/core/db.py`.

### 11.1 Demo User Accounts

- First superuser from environment variables
- `maya.patel@studylink.demo`
- `liam.chen@studylink.demo`
- `sofia.garcia@studylink.demo`

Default demo password:

- `DemoPass123!`

### 11.2 Demo Researcher Profiles

The database initializer seeds researcher profiles like:

- Dr. Alice Brown
- Dr. John Smith
- Dr. Sarah Johnson
- Dr. Michael Chen

### 11.3 Demo Publications

Seeded topics include:

- computer vision
- deep learning
- NLP
- robotics
- responsible AI

### 11.4 Demo Projects

Example seeded projects:

- StudyLink Demo Command Center
- Clinical Vision Bench
- Policy Aligned AI Toolkit

### 11.5 Demo Chats

Several seeded conversations are created so the chat module is already populated during demo or evaluation.

## 12. Installation and Setup

### 12.1 Prerequisites

- Docker
- Docker Compose
- Python environment support via `uv`
- Node.js and npm

### 12.2 Environment Configuration

Create or update the root `.env` file with values for:

```env
PROJECT_NAME=StudyLink
SECRET_KEY=your_secret_key
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=your_admin_password
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
FRONTEND_HOST=http://localhost:5173
ENVIRONMENT=local
```

Optional mail settings can be added for password reset support.

### 12.3 Running with Docker Compose

From the project root:

```bash
docker compose up --build
```

This starts:

- PostgreSQL database
- Adminer
- prestart service for migrations/init
- FastAPI backend
- frontend container

### 12.4 Backend Local Workflow

```bash
cd backend
uv sync
```

Run backend tests:

```bash
bash ./scripts/test.sh
```

### 12.5 Frontend Local Workflow

```bash
cd frontend
npm install
npm run dev
```

Frontend dev server default URL:

- `http://localhost:5173`

## 13. Database Migrations

Alembic migration files are stored in:

- `backend/app/alembic/versions/`

Typical commands:

```bash
cd backend
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

## 14. Testing

### 14.1 Backend Testing

Backend tests are written with Pytest and located in `backend/tests/`.

Coverage includes:

- CRUD tests
- route tests
- startup-related tests

### 14.2 Frontend Testing

Frontend tests use Playwright and are located in `frontend/tests/`.

Examples include:

- login
- signup
- reset password
- user settings

## 15. Deployment Notes

The repository includes:

- `docker-compose.yml`
- `docker-compose.override.yml`
- `docker-compose.traefik.yml`
- `deployment.md`

Production-style deployment uses:

- Traefik for routing and TLS
- separate frontend and backend services
- domain-based routing such as `api.<domain>` and `dashboard.<domain>`

## 16. Current Strengths of the Project

- clear separation between API, CRUD, models, and schemas
- meaningful seeded data for demo and evaluation
- modern frontend stack with query-based data fetching
- project and researcher modules are already shaped around a real academic use case
- realtime chat integration is functional and tied into frontend cache updates
- role-based admin protection exists for user management

## 17. Current Limitations and Improvement Opportunities

This is especially useful for black-book discussion.

- Some documentation files still reflect the original FastAPI template and not the final StudyLink domain
- There are traces of an older or alternate chat model in `backend/app/models/chats.py` and related docs, while the active app uses `backend/app/models/chat.py` plus `backend/app/models/message.py`
- The dashboard feed currently uses dummy paper data rather than a fully backend-driven paper feed
- Project member display on the frontend is still basic and does not show rich user profile info
- Some frontend pages such as notifications/messages are more placeholder-oriented than complete feature modules
- The current realtime system uses in-memory connection management, so horizontal scaling would need Redis or another shared broker
- Search is functional but can be improved with stronger filtering, ranking, and pagination strategies

## 18. Suggested Black Book Topics

If your friend is writing a black book, these are the strongest sections to expand from this project:

- introduction and problem definition
- objectives and scope
- requirement analysis
- system architecture
- module design
- database design and entity relationships
- API design
- authentication and security
- UI design and route structure
- realtime messaging workflow
- testing strategy
- deployment strategy
- limitations and future enhancements

## 19. Future Enhancements

- add richer publication management from the frontend
- add project editing UI and richer collaborator role management
- add notification backend and frontend integration
- add researcher-to-project linking
- add file upload support for project resources and chat attachments
- add message read receipts and typing indicators end to end
- add advanced search with ranking and recommendation logic
- add distributed realtime infrastructure for multi-instance deployment

## 20. Conclusion

StudyLink is a research collaboration platform that combines academic discovery, profile management, project coordination, and realtime communication in one application. The backend is structured cleanly around FastAPI and SQLModel, while the frontend uses a modern React stack with route-based pages and query-driven state management. The project is already strong enough for academic documentation because it includes domain-specific modules, seeded demo content, authentication, search, project workflows, and realtime chat.

For detailed subsystem notes, also refer to:

- `backend/README.md`
- `frontend/README.md`
- `REALTIME_MESSAGING.md`
- `development.md`
- `deployment.md`
