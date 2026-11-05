---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Mindmap

The `todo-api` project grouped by what its code does.

```mermaid
mindmap
  root((todo-api))
    a1["API"]
      a2["app/main.py: creates FastAPI app"]
      a3["app/routes.py: HTTP routes"]
        a4["create_todo()"]
        a5["list_todos()"]
    a6["Data"]
      a7["app/models.py: Todo dataclass"]
        a8["Todo.create()"]
      a9["app/storage.py: in-memory list"]
        a10["add_todo()"]
        a11["all_todos()"]
    a12["Utilities"]
      a13["app/utils.py: now_iso()"]
```

The map shows three groups: the HTTP API, the todo data and storage, and a small time helper.

## Groups

- API: builds the app and exposes `POST /todos` and `GET /todos` (`app/main.py`, `app/routes.py`).
- Data: the `Todo` dataclass and the in-memory store behind it (`app/models.py`, `app/storage.py`).
- Utilities: a UTC timestamp helper (`app/utils.py`). `app/storage.py` also has `next_id()`, left out of the map.

## Not covered

All source files were read; `app/__init__.py` is empty. Nothing was skipped.
