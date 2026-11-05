---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# todo-api Architecture Overview

`todo-api` is a tiny FastAPI service that creates and lists todos. It keeps all data in a process-local Python list.

## Level 1: System context

```mermaid
flowchart LR
    client["API client"]:::external
    api["todo-api (FastAPI app)"]
    client -->|"HTTP"| api
    classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

An HTTP client calls the single `todo-api` service; there is no database or other external system in the code.

## Level 2: Containers

```mermaid
flowchart LR
    client["API client"]:::external
    server["uvicorn server"]:::external
    app["FastAPI app: app/main.py"]
    mem["In-memory list _TODOS: app/storage.py"]
    client -->|"HTTP"| server
    server -->|"ASGI"| app
    app -->|"calls"| mem
    classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

The README starts the service with `uvicorn app.main:app`; uvicorn hands requests to the FastAPI `app`, which reads and writes the `_TODOS` list in `app/storage.py`. Persistence ends when the process stops, because no file or database is used.

## Level 3: Components

```mermaid
flowchart TD
    main["main: app/main.py"]
    routes["routes: app/routes.py"]
    models["models: app/models.py"]
    storage["storage: app/storage.py"]
    utils["utils: app/utils.py"]
    models <-->|"import cycle"| storage
    main -->|"include_router"| routes
    routes -->|"add_todo, all_todos"| storage
    routes -->|"now_iso"| utils
    linkStyle 0 stroke:#C62F3E,stroke-width:3px
    classDef cycle fill:#FDECEE,stroke:#C62F3E,color:#7A1823
    class models,storage cycle
```

`app/main.py` builds the app and mounts the router from `app/routes.py`; the router calls `app/storage.py` and `app/utils.py`. `app/models.py` and `app/storage.py` import each other, a deliberate cycle noted in the code comments.

| Component | Responsibility |
|---|---|
| `app/main.py` | Creates `FastAPI(title="todo-api")` and includes the router |
| `app/routes.py` | `POST /todos` (validates a non-blank title) and `GET /todos` |
| `app/models.py` | `Todo` dataclass with `to_dict()` and `create()` |
| `app/storage.py` | `_TODOS` list, `next_id()`, `add_todo()`, `all_todos()` |
| `app/utils.py` | `now_iso()` returns the current UTC time as ISO text |

## Not covered

Every file in the repository was read, including the empty `app/__init__.py`. Nothing was executed, so runtime behavior was not tested.
