---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---

<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->


# Mindmap

`todo-api` at a glance: four responsibilities, each backed by one small file.

```mermaid
mindmap
  root((todo-api))
    a1["App setup"]
      a2["app/main.py: creates FastAPI app, mounts router"]
    a3["API"]
      a4["app/routes.py: HTTP routes"]
        a5["create_todo()"]
        a6["list_todos()"]
    a7["Domain and storage"]
      a8["app/models.py: Todo dataclass"]
        a9["Todo.create()"]
      a10["app/storage.py: in-memory list"]
        a11["add_todo()"]
        a12["all_todos()"]
    a13["Utilities"]
      a14["app/utils.py: timestamps"]
        a15["now_iso()"]
```

Every branch maps to a file in `app/`; the leaves are the public functions that matter.

## Groups

- **App setup**: `app/main.py` builds the `FastAPI` instance and includes the router.
- **API**: `app/routes.py` exposes `POST /todos` and `GET /todos`.
- **Domain and storage**: `app/models.py` defines `Todo`; `app/storage.py` keeps todos in a module-level list. Left out: `to_dict()` and `next_id()`.
- **Utilities**: `app/utils.py` returns the current UTC time as an ISO string.

## Not covered

All Python files were read completely; `app/__init__.py` is empty. Nothing was skipped.
