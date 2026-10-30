# fastapi-production-starter

Production-style FastAPI backend starter — JWT auth, SQLAlchemy with MySQL, Redis caching, Docker setup and a pytest suite structure.

## Features

- JWT authentication with an auth router stub (`/auth/token` issues a token for a username).
- SQLAlchemy database layer configured for MySQL via `DATABASE_URL`.
- Redis caching helper: cached responses are stored with a time-to-live and served from cache on repeat requests.
- Health endpoint at `GET /health`.
- Settings loaded from environment variables with Pydantic.
- Docker setup for running the API together with MySQL and Redis.
- Pytest suite structure for testing the health and auth endpoints.

## Project structure

```
.
├── main.py            # FastAPI app, settings, auth router stub, health endpoint, cache helper
├── requirements.txt   # Dependencies
├── README.md
├── Dockerfile         # (add for container builds)
├── docker-compose.yml # (add for API + MySQL + Redis)
└── tests/
    ├── test_health.py
    └── test_auth.py
```

The `Dockerfile`, `docker-compose.yml` and `tests/` entries above describe the intended layout for extending this starter; the runnable core in this repository is `main.py`.

## Configuration

Set these environment variables (defaults are for local development only):

- `DATABASE_URL` — SQLAlchemy URL, for example `mysql+pymysql://user:password@localhost:3306/app_db`.
- `REDIS_URL` — Redis URL, for example `redis://localhost:6379/0`.
- `SECRET_KEY` — secret used to sign JWTs. Change this in production.

## How to run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## How to run with Docker

```bash
docker compose up --build
```

This starts the API with MySQL and Redis services. The API is then available at http://127.0.0.1:8000, with interactive docs at http://127.0.0.1:8000/docs.

## Endpoints

- `GET /health` — service health check.
- `POST /auth/token` — issue a JWT for a username (stub: replace with real user lookup and password checking).
- `GET /me` — example protected endpoint; requires a bearer token.
- `GET /cached/{key}` — example Redis-cached endpoint.

## Stack

Python, FastAPI, SQLAlchemy, MySQL, Redis, Pydantic, python-jose, Uvicorn, pytest.
