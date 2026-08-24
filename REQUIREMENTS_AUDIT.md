# Assignment 1 Requirements Audit

This audit is against the FlyRank Assignment 1 CRUD API requirements supplied for this project.

| Requirement | Current implementation/evidence |
|---|---|
| FastAPI CRUD API | `main.py` |
| `GET /` identifies API | Implemented and tested |
| `GET /health` returns `{"status":"ok"}` | Implemented and tested |
| Exactly three starter tasks | `main.py` seed list; test suite verifies list size |
| `GET /tasks` and `GET /tasks/{id}` | Implemented; unknown ID returns JSON `404` |
| `POST /tasks` | `201`; server assigns next ID and `done:false`; invalid/missing/blank title returns `400` |
| `PUT /tasks/{id}` | Title and/or done accepted; invalid body `400`; unknown ID `404` |
| `DELETE /tasks/{id}` | `204` with empty body; unknown ID `404` |
| Swagger `/docs` | Implemented by FastAPI and verified through an executed full CRUD cycle |
| Full curl CRUD evidence | `docs/curl-cycle.txt` plus the current GitHub Actions submission gate |
| Swagger screenshot | `docs/swagger-ui.png` |
| Swagger full CRUD evidence | `docs/swagger-cycle.txt` |
| Public repository | `NiknaxTheGreek/flyrank-backend-assignment-1-ai` |
| Meaningful stage history | Existing Stage 2–6 commits plus earlier setup work are preserved; audit work does not rewrite history |
| README install/run/API/evidence | Root `README.md` |
| Clean-user reproducibility | `.github/workflows/a1-submission-gate.yml` installs from a clean GitHub Actions checkout before testing |

## Definition of done

The technical Assignment 1 submission is considered ready only after the current `Assignment 1 Submission Gate` passes on the audit pull request. The separate project-level AI Rematch/comparison stage is intentionally not claimed here.
