---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 61c8a137934bf8b4447aea934667b3bbc4522f3b3d5e774f063bc32b5a76da7c, docs/codemap/dependency-graph.md: 0f85b06098ee0b4b1648fcf1428f98cd9063569d79c679efc70e3a6d9ec8c130, docs/codemap/mindmap.md: d5a86612648e8176ef5496d87a9cc46dbea460e4aadb64fbf37b570dc1ec1100, docs/codemap/sequence-flow.md: d6f9852d22fcfb6d912ba803222e5e670c43014294d2cdeab521d2d0b7dd4f16}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# todo-api Presentation Outline

## Slide 1: What is todo-api?

- A tiny FastAPI service for managing todos
- Two endpoints: `POST /todos`, `GET /todos`
- Run with `uvicorn app.main:app`

## Slide 2: Architecture

- Client, then uvicorn, then the FastAPI app in `app/main.py`
- Data lives in an in-memory list in `app/storage.py`
- Diagram: Level 2 in `architecture.md`

## Slide 3: Code layout

- Five modules in `app/`: main, routes, models, storage, utils
- Diagram: `mindmap.md`

## Slide 4: Creating a todo

- Blank titles are rejected with 422
- Timestamp, id and storage happen in `app/utils.py`, `app/models.py`, `app/storage.py`
- Diagram: scenario 1 in `sequence-flow.md`

## Slide 5: Watch out for

- `app/models.py` and `app/storage.py` import each other (deliberate cycle), see `dependency-graph.md`
- Data is lost on restart; ids are `len + 1`

## Slide 6: Where to start reading

- `README.md`, `app/main.py`, `app/routes.py`, `app/storage.py`; full order in `design-doc.md`

## Not covered

This outline condenses the existing codemap files and did not re-read the code. Nothing was executed.
