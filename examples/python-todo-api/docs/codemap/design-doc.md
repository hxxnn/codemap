---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731, docs/codemap/architecture.md: c940a044ff8cd39d09f2b8360bea94ffe130ceb79427ba4cac36246569394d0f, docs/codemap/dependency-graph.md: 40e7f7ff2816a8a0553c2e6197e20cc72d99cd5329a16975706b25e406188ce5, docs/codemap/mindmap.md: f2df21d103826f87a26c70e7c77135c26f38ada6760c8772ee083c027d8839f4, docs/codemap/sequence-flow.md: 72dc6439fcf2c9ad71f07485cfcb7fd6a853ce74e2956e58e7a814b3383b5e9f}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Design doc and onboarding guide

How `todo-api` is built and in what order to read it.

## Overview

`todo-api` is a small FastAPI service for managing todos (`README.md`). It exposes `POST /todos` to create a todo and `GET /todos` to list them. Todos live in memory, so they are lost when the process stops. It is written in Python, depends on `fastapi` and `uvicorn` (`pyproject.toml`), and starts with `uvicorn app.main:app`.

## How it is structured

The code is one package, `app/`, in three layers: an HTTP layer (`app/main.py`, `app/routes.py`), a data layer (`app/models.py`, `app/storage.py`) and a helper (`app/utils.py`). See `architecture.md` for the diagrams, `dependency-graph.md` for imports, `mindmap.md` for the overview and `sequence-flow.md` for the request flows. Requests enter through the router, and the route functions call storage directly. Storage and the `Todo` model import each other.

## Key design choices

1. **In-memory storage behind a small module.** The list `_TODOS` is private to `app/storage.py`, and routes use only `add_todo` and `all_todos`. Effect: persistence could be swapped in one file, but data is lost on restart. The reason is not stated in the code. (inferred) <!-- codemap:unverified -->
2. **Router separate from app setup.** `app/routes.py` defines an `APIRouter`, and `app/main.py` mounts it with `include_router`. Effect: routes can grow without touching app setup.
3. **Dataclass model with `to_dict`.** `Todo` in `app/models.py` is a `@dataclass` and routes return `todo.to_dict()`. Effect: responses are plain dicts rather than FastAPI response models.
4. **Deliberate circular import.** `app/models.py` and `app/storage.py` import each other, and both files have a comment saying it is deliberate. Effect: it works because each uses the other only inside functions; it is fragile to refactors. The reason for the cycle is not given. (inferred) <!-- codemap:unverified -->
5. **Input validation in the route.** `create_todo` rejects blank titles with a 422 error in `app/routes.py`, before storage is touched.

## Reading order (onboarding guide)

1. `README.md`: purpose and the run command.
2. `pyproject.toml`: dependencies (`fastapi`, `uvicorn`).
3. `app/main.py`: where the app is created and the router mounted.
4. `app/routes.py`: the two endpoints and the blank-title check.
5. `app/storage.py`: the in-memory list and its three functions; note the import of `models`.
6. `app/models.py`: the `Todo` dataclass and `Todo.create`, which calls back into storage for the id.
7. `app/utils.py`: `now_iso()`, the UTC timestamp helper.

## Not covered

All source files were read. `app/__init__.py` is empty. There are no tests, config files or deployment files in the repository.
