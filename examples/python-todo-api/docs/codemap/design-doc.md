---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, docs/codemap/architecture.md: ad44b98013f1df7780a691a4c18fc91f6769cb417e43326282166b05e3fc8313, docs/codemap/dependency-graph.md: b7c70a3167141b14ea591f3e957250d834392b054a7e498e361e856f2183def6, docs/codemap/mindmap.md: 8c7e1a314c8a6d850316783f913c07abcc450aac009300883c8a422e7fa23550, docs/codemap/sequence-flow.md: ccaa5237f6f2457f03fe5a39ba24af9fbf58926cef8e3aa904619e6f7ae79b66}
---

# Design doc and onboarding guide

## Overview

`todo-api` is a tiny service for managing todos (`README.md`). It is written in Python with FastAPI and served by uvicorn (`pyproject.toml`). It exposes two endpoints, `POST /todos` and `GET /todos`, and keeps all data in memory.

## How it is structured

One process holds everything: `app/main.py` creates the app and mounts the router from `app/routes.py`; the routes call `app/storage.py`, which stores `Todo` objects defined in `app/models.py`; `app/utils.py` supplies timestamps. See `architecture.md` for the three zoom levels, `mindmap.md` for the overview tree, `sequence-flow.md` for the request flows and `dependency-graph.md` for imports.

## Key design choices

1. **In-memory storage behind a small module.** Todos live in the module-level list `_TODOS` in `app/storage.py`, exposed only through `add_todo`, `all_todos` and `next_id`. Effect: no persistence, data is lost on restart. Reason: not stated in the code (inferred: keep the example simple). <!-- codemap:unverified -->
2. **Models and storage import each other.** `app/models.py` and `app/storage.py` form a cycle; both files carry a comment calling it deliberate (`dependency-graph.md`). It works because each only uses the other inside functions.
3. **IDs derived from list length.** `app/storage.py:next_id` returns `len(_TODOS) + 1`, so ids are sequential and would collide if items were ever removed. Reason not stated. <!-- codemap:unverified -->
4. **Validation in the route.** `app/routes.py:create_todo` rejects blank titles with HTTP 422 and strips whitespace before storing.
5. **One router, wired in the entry file.** `app/main.py` only builds `FastAPI(title="todo-api")` and includes the router; all endpoints are in `app/routes.py`.

## Reading order (onboarding guide)

1. `README.md`: purpose and the run command.
2. `pyproject.toml`: dependencies (`fastapi`, `uvicorn`).
3. `app/main.py`: where the app is created and the router attached.
4. `app/routes.py`: the two endpoints and the title validation.
5. `app/storage.py`: how todos are stored and how ids are made.
6. `app/models.py`: the `Todo` dataclass and `Todo.create`; note the import cycle with storage.
7. `app/utils.py`: `now_iso`, the timestamp helper.

## Not covered

All Python files, `pyproject.toml` and `README.md` were read completely. `app/__init__.py` is empty. The repo has no tests or deployment config. FastAPI/uvicorn internals were not examined.
