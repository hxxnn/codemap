---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---

# Sequence flows

Two runtime scenarios traced through the code: creating a todo (including its validation error path) and listing todos.

## Create a todo (POST /todos)

Triggered when a client posts to `/todos` with a `title`; this is the main write operation and it touches storage and the model.

```mermaid
sequenceDiagram
  participant C as HTTP client
  participant F as FastAPI (app/main.py)
  participant R as app/routes.py
  participant U as app/utils.py
  participant S as app/storage.py
  participant M as app/models.py
  C->>F: POST /todos
  F-->>R: dispatch (not traced)
  Note over F,R: framework routing, not traced
  R->>R: create_todo(title)
  alt title is blank
    R-->>C: HTTPException 422 "title required"
  else title present
    R->>U: now_iso()
    U-->>R: ISO timestamp
    R->>S: add_todo(title.strip(), created_at)
    S->>M: Todo.create(title, created_at)
    M->>S: next_id()
    S-->>M: len(_TODOS) + 1
    M-->>S: Todo
    S->>S: _TODOS.append(todo)
    S-->>R: Todo
    R-->>C: todo.to_dict()
  end
```

The route validates the title, stamps the time, and storage asks the model to build a `Todo` whose id comes back from storage.

1. Client sends the request; `app/main.py` registered the router via `app.include_router(router)`.
2. FastAPI calls `app/routes.py:create_todo`.
3. If `title.strip()` is empty it raises `HTTPException(422)`: `app/routes.py:create_todo`.
4. Otherwise it gets a timestamp: `app/utils.py:now_iso`.
5. It calls `app/storage.py:add_todo`.
6. Storage calls `app/models.py:Todo.create`, which calls `app/storage.py:next_id`.
7. Storage appends the todo to `_TODOS` and returns it; the route returns `Todo.to_dict()` (`app/models.py:Todo.to_dict`).

The framework dispatch step is not traced because FastAPI's internals were not read. <!-- codemap:unverified -->

## List todos (GET /todos)

Triggered when a client requests `/todos`; it only reads from storage.

```mermaid
sequenceDiagram
  participant C as HTTP client
  participant R as app/routes.py
  participant S as app/storage.py
  C->>R: GET /todos (via FastAPI, not traced)
  R->>S: all_todos()
  S-->>R: list copy of _TODOS
  R-->>C: [t.to_dict() for t in todos]
```

The route copies the stored list and serialises each `Todo`.

1. FastAPI calls `app/routes.py:list_todos`.
2. It calls `app/storage.py:all_todos`, which returns `list(_TODOS)`.
3. Each item is converted with `app/models.py:Todo.to_dict`.

## Not covered

All Python files were read completely. FastAPI/uvicorn internals (routing, parameter parsing) were not traced.
