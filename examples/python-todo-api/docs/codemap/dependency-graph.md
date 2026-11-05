---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {app/__init__.py: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---

<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->


# Dependency graph

Internal imports between the Python files of `todo-api`; each arrow points from the importer to the imported file.

```mermaid
flowchart LR
  n1["app/main.py"]
  n2["app/routes.py"]
  n3["app/models.py"]
  n4["app/storage.py"]
  n5["app/utils.py"]
  n1 --> n2
  n2 --> n4
  n2 --> n5
  n3 --> n4
  n4 --> n3
  linkStyle 3,4 stroke:#d33,stroke-width:3px
```

Red edges mark the one import cycle; third-party imports (`fastapi`, `dataclasses`, `datetime`) are omitted.

## Circular dependencies

- `app/models.py` → `app/storage.py` → `app/models.py`

Both files carry a comment calling the cycle deliberate. Each file only uses the other's attributes inside functions, so the cycle does not fail at import time.

## Most depended-on files

- `app/storage.py`: imported by `app/routes.py` and `app/models.py` (2 incoming)
- `app/models.py`: imported by `app/storage.py` (1 incoming)
- `app/routes.py`: imported by `app/main.py` (1 incoming)
- `app/utils.py`: imported by `app/routes.py` (1 incoming)

## Not covered

All Python files were read completely; `app/__init__.py` is empty and has no imports. No dynamic imports were found.
