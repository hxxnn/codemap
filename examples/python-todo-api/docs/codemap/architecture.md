---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {app/__init__.py: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731}
---

# Architecture overview

`todo-api` is a tiny FastAPI service (see `pyproject.toml`, `README.md`) shown here at three zoom levels.

## Level 1: System context

```mermaid
flowchart LR
  client["HTTP client (inferred)"]
  sys["todo-api (FastAPI service)"]
  client -->|"POST and GET /todos"| sys
```

The service is one system reached over HTTP; no database or third-party API is referenced anywhere in the code.

The HTTP client is inferred from the routes in `app/routes.py`; no client code exists in the repo. <!-- codemap:unverified -->

## Level 2: Containers

```mermaid
flowchart LR
  client["HTTP client (inferred)"]
  subgraph proc["uvicorn process (README.md)"]
    api["FastAPI app (app/)"]
    mem["In-memory list _TODOS (app/storage.py)"]
  end
  client -->|"HTTP"| api
  api -->|"function calls"| mem
```

There is a single deployable process, started with `uvicorn app.main:app` per `README.md`; todos live in a module-level list inside it, so they are lost on restart.

## Level 3: Components

```mermaid
flowchart TD
  subgraph entry["Entry"]
    main["App setup (app/main.py)"]
  end
  subgraph web["HTTP layer"]
    routes["Routes (app/routes.py)"]
  end
  subgraph domain["Domain and data"]
    models["Todo dataclass (app/models.py)"]
    storage["In-memory store (app/storage.py)"]
  end
  subgraph helpers["Helpers"]
    utils["now_iso (app/utils.py)"]
  end
  main -->|"include_router"| routes
  routes -->|"add_todo, all_todos"| storage
  routes -->|"now_iso"| utils
  storage -->|"Todo.create"| models
  models -->|"next_id"| storage
```

`app/main.py` mounts the router from `app/routes.py`, which delegates persistence to `app/storage.py`; `app/models.py` and `app/storage.py` import each other (a deliberate cycle per the comments in both files).

## Not covered

All 6 Python files, `pyproject.toml` and `README.md` were read completely. `app/__init__.py` is empty. There are no tests, config files or deployment files in the repo. Nothing was skipped.
