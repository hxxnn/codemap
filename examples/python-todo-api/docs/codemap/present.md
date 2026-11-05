---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: ad44b98013f1df7780a691a4c18fc91f6769cb417e43326282166b05e3fc8313, docs/codemap/dependency-graph.md: b7c70a3167141b14ea591f3e957250d834392b054a7e498e361e856f2183def6, docs/codemap/mindmap.md: 8c7e1a314c8a6d850316783f913c07abcc450aac009300883c8a422e7fa23550, docs/codemap/sequence-flow.md: 7abd52c457917a4890452a66f0aeba6999fe33519834ed2460393ba3f616ba18, docs/codemap/design-doc.md: 15212f1f451ac76f67b47ab1323e5bef0ccc368b71108c9ab6873c6fb4d7f836}
---

# Presentation outline

Seven slides explaining `todo-api`, built only from the other codemap artifacts (all five were present).

## Slide 1: What it is
`todo-api` is a tiny FastAPI service for managing todos, run with uvicorn. It has two endpoints and keeps data in memory.
Show: `design-doc.md` → "Overview"

## Slide 2: The big picture
One uvicorn process holds the FastAPI app and an in-memory list of todos. The HTTP client is inferred, not present in the repo. <!-- codemap:unverified -->
Show: `architecture.md` → "Level 2: Containers" diagram

## Slide 3: How it is organized
Four responsibilities, each in one small file under `app/`: app setup, API, domain and storage, utilities.
Show: `mindmap.md` → "Mindmap" diagram

## Slide 4: How it runs
`POST /todos` validates the title, stamps the time, then storage asks the model to build a `Todo` and appends it. A blank title returns 422.
Show: `sequence-flow.md` → "Create a todo (POST /todos)" diagram

## Slide 5: How the parts depend on each other
Five files with simple imports, except one deliberate cycle: `app/models.py` and `app/storage.py` import each other.
Show: `dependency-graph.md` → "Dependency graph" diagram and "Circular dependencies"

## Slide 6: Key design choices
Storage is an in-memory list, so data is lost on restart; the reason is inferred, not stated. <!-- codemap:unverified --> Ids come from list length, which would collide if items were ever removed; the reason is also inferred. <!-- codemap:unverified -->
Show: `design-doc.md` → "Key design choices"

## Slide 7: Where to start reading
Start with `README.md`, then `app/main.py`, `app/routes.py` and `app/storage.py`.
Show: `design-doc.md` → "Reading order (onboarding guide)"

## Not covered

All Python files, `pyproject.toml` and `README.md` were read completely. The repo has no tests or deployment config, and FastAPI/uvicorn internals were not examined.
