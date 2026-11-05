---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# todo-api Mindmap

## Project at a glance

```mermaid
mindmap
  root((todo-api))
    n1["app/"]
      n2["main.py: creates FastAPI app"]
      n3["routes.py: POST and GET /todos"]
      n4["models.py: Todo dataclass"]
      n5["storage.py: in-memory list"]
      n6["utils.py: now_iso"]
      n7["__init__.py: empty"]
    n8["pyproject.toml: fastapi, uvicorn"]
    n9["README.md: run with uvicorn"]
```

The whole project is one `app/` package with five working modules, plus a manifest and a short README.

## Not covered

Every file in the repository was read.
