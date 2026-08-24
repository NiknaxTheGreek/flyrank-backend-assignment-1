# FlyRank Backend Assignment 1 — CRUD API

A small FastAPI server that manages an in-memory to-do list with full CRUD operations. Data intentionally lives only in memory for Assignment 1 and resets when the process restarts.

## Install and run

Requires Python 3.10+.

From a clean clone:

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

The API listens on `http://localhost:8000`; Swagger UI is at `http://localhost:8000/docs`.

## API contract

| Method | Path | Success | Failure behavior | Purpose |
|---|---|---:|---|---|
| GET | `/` | 200 | — | Identify the API |
| GET | `/health` | 200 | — | Return `{"status":"ok"}` |
| GET | `/tasks` | 200 | — | List all tasks |
| GET | `/tasks/{id}` | 200 | 404 unknown ID | Get one task |
| POST | `/tasks` | 201 | 400 missing/blank/invalid title | Create a task; server assigns ID and `done:false` |
| PUT | `/tasks/{id}` | 200 | 400 invalid body; 404 unknown ID | Update `title` and/or `done` |
| DELETE | `/tasks/{id}` | 204 | 404 unknown ID | Delete a task with an empty response body |

The process starts with exactly three in-memory tasks using the `id`, `title`, and `done` fields.

## Verification evidence

The final repository contains executed evidence rather than sample-only commands:

- [`docs/curl-cycle.txt`](docs/curl-cycle.txt) — recorded `curl -i` CRUD lifecycle output.
- [`docs/swagger-cycle.txt`](docs/swagger-cycle.txt) — records the full CRUD sequence executed through Swagger UI `Try it out` / `Execute`, including the observed `200`, `201`, and `204` responses and post-operation checks.
- [`docs/swagger-ui.png`](docs/swagger-ui.png) — Swagger UI screenshot from that verification run.
- [`docs/test-results.txt`](docs/test-results.txt) — recorded automated-test result.
- [`.github/workflows/a1-submission-gate.yml`](.github/workflows/a1-submission-gate.yml) — clean-checkout acceptance gate that reinstalls dependencies, runs the contract tests, starts the real server, performs a complete curl lifecycle, and verifies the Swagger evidence.

Example from the recorded curl evidence:

```text
POST /tasks -> 201
PUT /tasks/{id} -> 200
DELETE /tasks/{id} -> 204
GET deleted task -> 404
```

## Swagger UI

![Swagger UI showing the Task API endpoints](docs/swagger-ui.png)

## Tests

```bash
pytest -q
```

The automated suite checks the exact root/health payloads, the three-task in-memory schema, CRUD success codes, `400` validation, `404` JSON errors, partial updates, empty `204` delete responses, and generated Swagger/OpenAPI descriptions.

## Git history

The repository contains the Assignment 1 stage commits, including Stage 2 read endpoints, Stage 3 create/validation, Stage 4 full CRUD, Stage 5 Swagger UI, and Stage 6 publish/docs, plus later evidence-only and audit fixes. These existing commits are preserved; the final audit does not rewrite history.

## In-memory limitation

Because Assignment 1 deliberately uses in-memory storage, tasks created while the server is running disappear when the process restarts. Assignment 2 introduces persistent database storage to solve that limitation.
