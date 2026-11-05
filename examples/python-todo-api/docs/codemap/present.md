---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 68841850f67409cc0e28deb9cd2ef8915a881af22914d42386ba32cb448d67af, docs/codemap/dependency-graph.md: 0ced1e95e249a6a88e3d187a14261d340a631389fc33fdb830b8a3cf5a6d0b8b, docs/codemap/mindmap.md: c820de42460c97d8cdf63025da716aa59752566b8cfc40a6e89e0f625fc652a3, docs/codemap/sequence-flow.md: 8b78738ef8a1177f90d626af83b4dc616d9c1fade2120b95f2e4967b0fc3acda, docs/codemap/design-doc.md: 4098576aae2c19ef2edcc49d2910071a60fe1f4ff2bd4cf0920f4748e0ea7d2f}
---

<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->


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
