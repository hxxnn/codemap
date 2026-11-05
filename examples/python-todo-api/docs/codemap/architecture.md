---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Architecture overview

`todo-api` is a tiny FastAPI service that keeps todos in memory, shown at three zoom levels.

## System context

```mermaid
flowchart TD
    n1["API client (HTTP)"]:::external
    n2["todo-api (FastAPI service)"]
    n1 -->|"POST /todos, GET /todos"| n2
    classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

Callers send HTTP requests to the single `todo-api` service; no database or third-party API is referenced in the code.

## Containers

```mermaid
flowchart TD
    n1["API client (HTTP)"]:::external
    subgraph n2["todo-api process (uvicorn app.main:app)"]
        n3["FastAPI app (Python, app/)"]
        n4["In-memory todo list (_TODOS in app/storage.py)"]
    end
    n1 -->|"HTTP"| n3
    n3 -->|"function calls"| n4
    classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

The service is one Python process (run command from `README.md`, dependencies from `pyproject.toml`) whose only state is a module-level list in `app/storage.py`.

## Components

```mermaid
flowchart TD
    subgraph web["HTTP layer"]
        main["App setup (app/main.py)"]
        routes["Routes (app/routes.py)"]
    end
    subgraph domain["Domain and data"]
        models["Todo model (app/models.py)"]
        storage["Storage (app/storage.py)"]
    end
    utils["Time helper (app/utils.py)"]
    main -->|"include_router"| routes
    routes -->|"add_todo, all_todos"| storage
    routes -->|"now_iso"| utils
    storage -->|"Todo.create"| models
    models -->|"next_id"| storage
```

`app/main.py` mounts the router from `app/routes.py`, which delegates to `app/storage.py`; storage and `app/models.py` call each other (a deliberate cycle, see `dependency-graph.md`).

## Not covered

All source files were read (`app/__init__.py` is empty). Nothing was skipped; deployment, tests and CI do not exist in the repository.
