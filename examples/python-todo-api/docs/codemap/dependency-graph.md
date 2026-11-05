---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# todo-api Dependency Graph

This graph comes from the real `import` statements in `app/`. It shows one circular dependency.

## Internal import graph

```mermaid
flowchart LR
    models["app/models.py"]
    storage["app/storage.py"]
    main["app/main.py"]
    routes["app/routes.py"]
    utils["app/utils.py"]
    fastapi["fastapi"]:::external
    models -->|"imports"| storage
    storage -->|"imports"| models
    main -->|"imports"| routes
    routes -->|"imports"| storage
    routes -->|"imports"| utils
    main --> fastapi
    routes --> fastapi
    linkStyle 0 stroke:#C62F3E,stroke-width:3px
    linkStyle 1 stroke:#C62F3E,stroke-width:3px
    classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
    classDef cycle fill:#FDECEE,stroke:#C62F3E,color:#7A1823
    class models,storage cycle
```

An arrow means "imports". `app/main.py` leads to `app/routes.py`, which uses `app/storage.py` and `app/utils.py`; `fastapi` is the only third-party import. The standard library (`dataclasses`, `datetime`) is left out.

## Circular dependency

- `app/models.py` has `from app import storage` and `app/storage.py` has `from app import models`. Both files mark the cycle as deliberate in a comment.
- The cycle is only used inside function bodies (`storage.next_id()` in `Todo.create`, `models.Todo.create` in `add_todo`), not at import time. <!-- codemap:unverified --> (inferred from reading; the app was not run to confirm the import order works)

## Not covered

All five Python modules were read. `app/__init__.py` is empty. Standard-library and installed-package internals were not examined.
