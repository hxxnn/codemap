---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, app/__init__.py: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Dependency graph

Import edges between the project's own Python files, taken from the import statements that were read.

```mermaid
flowchart LR
    n1["app/main.py"]
    n2["app/routes.py"]
    n3["app/storage.py"]
    n4["app/models.py"]
    n5["app/utils.py"]
    n1 --> n2
    n2 --> n3
    n2 --> n5
    n3 --> n4
    n4 --> n3
    classDef cycle fill:#FDECEE,stroke:#C62F3E,color:#7A1823
    class n3,n4 cycle
    linkStyle 3 stroke:#C62F3E,stroke-width:3px
    linkStyle 4 stroke:#C62F3E,stroke-width:3px
```

Arrows point from importer to imported file; the red files and edges form a circular import.

## Circular dependencies

One cyclic group: `app/storage.py` and `app/models.py`. Example cycle: `app/storage.py` → `app/models.py` → `app/storage.py`. Both files carry a comment calling the cycle deliberate. It works because each module only uses the other inside functions, after both are loaded.

## Most depended-on files

- `app/storage.py`: imported by `app/routes.py` and `app/models.py` (2 incoming edges).
- `app/models.py`: imported by `app/storage.py` (1).
- `app/routes.py`: imported by `app/main.py` (1).
- `app/utils.py`: imported by `app/routes.py` (1).

## Not covered

Third-party imports (`fastapi`, `dataclasses`, `datetime`) are ignored. `app/__init__.py` is empty. All other source files were read; nothing was skipped.
