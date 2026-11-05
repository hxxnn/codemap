---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 61c8a137934bf8b4447aea934667b3bbc4522f3b3d5e774f063bc32b5a76da7c, docs/codemap/dependency-graph.md: 0f85b06098ee0b4b1648fcf1428f98cd9063569d79c679efc70e3a6d9ec8c130, docs/codemap/sequence-flow.md: d6f9852d22fcfb6d912ba803222e5e670c43014294d2cdeab521d2d0b7dd4f16, docs/codemap/mindmap.md: d5a86612648e8176ef5496d87a9cc46dbea460e4aadb64fbf37b570dc1ec1100}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# todo-api Design Document

## Overview

`todo-api` is a small FastAPI service with two endpoints: `POST /todos` creates a todo and `GET /todos` lists them. Python code lives in the `app/` package, and todos are kept in a module-level list in `app/storage.py`. See `architecture.md` for the diagrams.

## Key design choices

- **In-memory storage.** `_TODOS` in `app/storage.py` is a plain list, so data is lost when the process stops. There is no database dependency in `pyproject.toml`.
- **Thin layers.** `app/routes.py` handles HTTP and validation, `app/storage.py` holds data, `app/models.py` defines the `Todo` dataclass, and `app/utils.py` supplies the timestamp.
- **Deliberate import cycle.** `app/models.py` and `app/storage.py` import each other; both files say it is deliberate. See `dependency-graph.md`.
- **Ids come from list length.** `next_id()` returns `len(_TODOS) + 1`, so ids are sequential as long as nothing is ever removed (no delete exists today).
- **Why these choices were made** is not documented anywhere in the repository. <!-- codemap:unverified --> (design rationale is inferred, not stated in code)

## Request flow

A `POST /todos` request is validated in `app/routes.py`, timestamped by `app/utils.py`, built into a `Todo` through `app/storage.py` and `app/models.py`, stored, and returned as a dict. A `GET /todos` request returns a copy of the list. Diagrams are in `sequence-flow.md`.

## Reading order for newcomers

1. `README.md`: what the project is and how to run it (`uvicorn app.main:app`).
2. `pyproject.toml`: the dependencies (`fastapi`, `uvicorn`).
3. `app/main.py`: creates the app and mounts the router.
4. `app/routes.py`: the two endpoints.
5. `app/storage.py`: where the data lives.
6. `app/models.py`: the `Todo` shape and the import cycle with storage.
7. `app/utils.py`: the one-line timestamp helper.

## Not covered

All repository files were read; `app/__init__.py` is empty. No tests exist in the repository, and nothing was executed.
