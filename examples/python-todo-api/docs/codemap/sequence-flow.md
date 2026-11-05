---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 시퀀스 흐름

가장 중심인 `POST /todos`, 목록을 읽는 `GET /todos`, 그리고 제목이 비었을 때의 오류 경로, 이 세 가지 실행 흐름을 코드에서 따라가며 그렸습니다.

## POST /todos: 할 일 만들기

클라이언트가 `title`과 함께 `POST /todos`를 호출하면 시작됩니다.

```mermaid
sequenceDiagram
  participant C as 클라이언트
  participant F as FastAPI (app/main.py)
  participant R as app/routes.py
  participant U as app/utils.py
  participant S as app/storage.py
  participant M as app/models.py
  C->>F: POST /todos
  F-)R: create_todo(title)
  Note over F,R: 프레임워크의 라우팅 호출은 추적하지 않음
  R->>U: now_iso()
  U-->>R: ISO 시각 문자열
  R->>S: add_todo(title.strip(), created_at)
  S->>M: Todo.create(title, created_at)
  M->>S: next_id()
  S-->>M: len(_TODOS) + 1
  M-->>S: Todo
  S->>S: _TODOS.append(todo)
  S-->>R: Todo
  R->>M: todo.to_dict()
  M-->>R: dict
  R-)F: dict 반환
  Note over R,F: JSON 직렬화는 추적하지 않음
  F-->>C: 응답
```

라우터 함수 호출과 응답 직렬화는 FastAPI 내부 동작이라 따라가지 않았습니다(추정). <!-- codemap:unverified -->

1. `app/main.py`: `app.include_router(router)`로 등록된 라우트가 요청을 받습니다.
2. `app/routes.py:create_todo`: 제목이 비어 있지 않은지 검사합니다(아래 오류 흐름 참고).
3. `app/utils.py:now_iso`: UTC 현재 시각을 ISO 문자열로 만듭니다.
4. `app/storage.py:add_todo`: `Todo`를 만들어 `_TODOS`에 넣습니다.
5. `app/models.py:Todo.create`: `app/storage.py:next_id`로 id를 받아 `Todo`를 만듭니다.
6. `app/models.py:Todo.to_dict`: 응답용 dict로 바꿉니다.

## GET /todos: 목록 조회

클라이언트가 `GET /todos`를 호출하면 시작됩니다.

```mermaid
sequenceDiagram
  participant C as 클라이언트
  participant F as FastAPI (app/main.py)
  participant R as app/routes.py
  participant S as app/storage.py
  participant M as app/models.py
  C->>F: GET /todos
  F-)R: list_todos()
  Note over F,R: 프레임워크의 라우팅 호출은 추적하지 않음
  R->>S: all_todos()
  S-->>R: list(_TODOS)
  loop 각 Todo t
    R->>M: t.to_dict()
    M-->>R: dict
  end
  R-->>F: dict 목록
  F-->>C: 응답
```

저장소는 `list(_TODOS)`로 복사본을 돌려주므로 라우트가 원본 리스트를 직접 바꾸지 않습니다.

1. `app/routes.py:list_todos`: 목록 조회 라우트입니다.
2. `app/storage.py:all_todos`: `_TODOS`의 복사본을 반환합니다.
3. `app/models.py:Todo.to_dict`: 각 항목을 dict로 바꿔 리스트 컴프리헨션으로 모읍니다.

## POST /todos: 제목이 비었을 때

`title.strip()`이 빈 문자열이면 저장소를 거치지 않고 오류로 끝납니다.

```mermaid
sequenceDiagram
  participant C as 클라이언트
  participant F as FastAPI (app/main.py)
  participant R as app/routes.py
  C->>F: POST /todos (공백 제목)
  F-)R: create_todo(title)
  Note over F,R: 프레임워크의 라우팅 호출은 추적하지 않음
  alt not title.strip()
    R-->>F: HTTPException(422, "title required")
    F-->>C: 422 응답
  end
```

이 경우 `app/utils.py`, `app/storage.py`, `app/models.py`는 호출되지 않습니다.

1. `app/routes.py:create_todo`: `if not title.strip()` 조건에서 `HTTPException(status_code=422, detail="title required")`를 발생시킵니다.

## 다루지 않은 범위

`app/` 아래 모든 파일을 읽었습니다. FastAPI와 uvicorn 내부(요청 파싱, 라우팅, 직렬화)는 라이브러리 코드라 읽지 않았고, 실제로 서버를 실행해 확인하지도 않았습니다.
