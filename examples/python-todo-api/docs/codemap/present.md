---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: c940a044ff8cd39d09f2b8360bea94ffe130ceb79427ba4cac36246569394d0f, docs/codemap/dependency-graph.md: 40e7f7ff2816a8a0553c2e6197e20cc72d99cd5329a16975706b25e406188ce5, docs/codemap/mindmap.md: f2df21d103826f87a26c70e7c77135c26f38ada6760c8772ee083c027d8839f4, docs/codemap/sequence-flow.md: 72dc6439fcf2c9ad71f07485cfcb7fd6a853ce74e2956e58e7a814b3383b5e9f, docs/codemap/design-doc.md: 4faab1fc0cf13ef43d6571a26882771a0e2ace28b0a522ab5fda1781b5b6e0cc}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Presentation outline

A seven-slide walkthrough of `todo-api`, built from the existing codemap documents. All five source artifacts were available.

## Slide 1: What it is
`todo-api` is a tiny FastAPI service that creates and lists todos, kept in memory. It is written in Python with `fastapi` and `uvicorn`.
Show: `design-doc.md` → "Overview"

## Slide 2: The big picture
Clients call one HTTP service. Inside, the FastAPI app talks to a module-level list that holds all state.
Show: `architecture.md` → "Containers" diagram

## Slide 3: How it is organized
The code splits into three groups: API, Data and Utilities.
Show: `mindmap.md` → "Mindmap" diagram

## Slide 4: How it runs
`POST /todos` validates the title, takes a timestamp, and asks storage to add the todo. The model asks storage for the next id along the way.
Show: `sequence-flow.md` → "Create a todo" diagram

## Slide 5: How the parts depend on each other
Imports are shallow except for one circular import between `app/storage.py` and `app/models.py`, which the code comments call deliberate.
Show: `dependency-graph.md` → "Dependency graph" diagram and "Circular dependencies"

## Slide 6: Key design choices
Storage is an in-memory list hidden behind a small module; its rationale is inferred. <!-- codemap:unverified --> (inferred) The cycle between models and storage works only because each uses the other inside functions; the reason for it is inferred. <!-- codemap:unverified --> (inferred)
Show: `design-doc.md` → "Key design choices"

## Slide 7: Where to start reading
Start with `README.md`, then `app/main.py`, `app/routes.py` and `app/storage.py`.
Show: `design-doc.md` → "Reading order (onboarding guide)"

## Not covered

All source files were read, and `app/__init__.py` is empty. There are no tests, config or deployment files, and FastAPI's internal request handling is not traced.
