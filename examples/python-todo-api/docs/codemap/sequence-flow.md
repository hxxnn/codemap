---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Sequence flows

Three runtime scenarios traced through the code: creating a todo, rejecting an empty title, and listing todos.

## Create a todo

A client sends `POST /todos` with a non-empty `title`.

```mermaid
sequenceDiagram
    participant C as Client
    participant R as app/routes.py
    participant U as app/utils.py
    participant S as app/storage.py
    participant M as app/models.py
    C->>R: POST /todos (title)
    R->>U: now_iso()
    U-->>R: ISO timestamp
    R->>S: add_todo(title.strip(), created_at)
    S->>M: Todo.create(title, created_at)
    M->>S: next_id()
    S-->>M: len(_TODOS) + 1
    M-->>S: Todo
    S->>S: _TODOS.append(todo)
    S-->>R: Todo
    R->>R: todo.to_dict()
    R-->>C: dict
```

1. `app/routes.py:create_todo` checks the title, then calls `now_iso()` for the timestamp.
2. `app/utils.py:now_iso` returns the current UTC time as an ISO string.
3. `app/storage.py:add_todo` asks the model to build the todo.
4. `app/models.py:Todo.create` calls `app/storage.py:next_id` for the id.
5. `app/storage.py:add_todo` appends the todo to `_TODOS` and returns it.
6. `app/routes.py:create_todo` returns `todo.to_dict()` (`app/models.py:Todo.to_dict`).

## Create a todo with an empty title

A client sends `POST /todos` with a blank `title`.

```mermaid
sequenceDiagram
    participant C as Client
    participant R as app/routes.py
    C->>R: POST /todos (title)
    alt not title.strip()
        R-->>C: HTTPException 422 "title required"
    end
```

1. `app/routes.py:create_todo` strips the title and, if it is empty, raises `HTTPException(status_code=422, detail="title required")`. Storage is never called.

## List todos

A client sends `GET /todos`.

```mermaid
sequenceDiagram
    participant C as Client
    participant R as app/routes.py
    participant S as app/storage.py
    C->>R: GET /todos
    R->>S: all_todos()
    S-->>R: list copy of _TODOS
    R->>R: t.to_dict() for each todo
    R-->>C: list of dicts
```

1. `app/routes.py:list_todos` calls `app/storage.py:all_todos`, which returns a copy of the list.
2. `app/routes.py:list_todos` converts each todo with `app/models.py:Todo.to_dict` and returns the list.

Request routing from `app/main.py` (`app.include_router(router)`) is done by FastAPI and is not drawn.

## Not covered

All source files were read; `app/__init__.py` is empty. FastAPI's internal request handling is not traced.
