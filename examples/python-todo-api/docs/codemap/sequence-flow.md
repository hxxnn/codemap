---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# todo-api Sequence Flows

## Scenario 1: POST /todos (create a todo)

```mermaid
sequenceDiagram
    participant C as API client
    participant R as app/routes.py
    participant U as app/utils.py
    participant S as app/storage.py
    participant M as app/models.py
    C->>R: POST /todos (title)
    alt title is blank
        R-->>C: 422 title required
    else title present
        R->>U: now_iso()
        U-->>R: UTC timestamp
        R->>S: add_todo(title, created_at)
        S->>M: Todo.create(title, created_at)
        M->>S: next_id()
        S-->>M: len(_TODOS) + 1
        M-->>S: Todo
        S-->>R: Todo (appended to _TODOS)
        R-->>C: todo.to_dict()
    end
```

`create_todo` in `app/routes.py` rejects a blank title with HTTP 422. Otherwise it stamps the time, and `app/storage.py` asks `app/models.py` to build the `Todo` (which gets its id back from `app/storage.py`) before appending it to the list.

The `title` argument is a plain `str` parameter, which FastAPI treats as a query parameter. <!-- codemap:unverified --> (framework behavior, not run)

## Scenario 2: GET /todos (list todos)

```mermaid
sequenceDiagram
    participant C as API client
    participant R as app/routes.py
    participant S as app/storage.py
    C->>R: GET /todos
    R->>S: all_todos()
    S-->>R: copy of _TODOS
    R-->>C: list of to_dict() results
```

`list_todos` in `app/routes.py` copies the stored list through `all_todos()` and returns each todo as a dict.

## Not covered

All modules on both paths were read. Nothing was executed, so the HTTP-level behavior (status codes, parameter parsing) comes from reading the code only.
