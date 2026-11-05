---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 시퀀스 흐름

실제 코드를 따라가며 세 가지 시나리오를 그렸습니다. 고른 이유: (1) `POST /todos`는 가장 중심이 되는 쓰기 동작, (2) `GET /todos`는 저장소를 읽는 동작, (3) 빈 제목은 코드에 있는 유일한 오류 경로입니다. 열린 화살표(`-)`)는 FastAPI 프레임워크가 내부에서 처리해 따라가지 않은 구간입니다.

## POST /todos — 할 일 추가

클라이언트가 `POST /todos`로 제목을 보내면 `create_todo()`가 실행됩니다.

```mermaid
sequenceDiagram
  participant C as 클라이언트
  participant R as app/routes.py
  participant U as app/utils.py
  participant S as app/storage.py
  participant M as app/models.py
  C-)R: POST /todos
  Note over C,R: FastAPI의 라우팅 호출은 추적하지 않음
  R->>R: create_todo(title) 검사
  R->>U: now_iso()
  U-->>R: ISO 시각 문자열
  R->>S: add_todo(title.strip(), created_at)
  S->>M: Todo.create(title, created_at)
  M->>S: next_id()
  S-->>M: len(_TODOS) + 1
  M-->>S: Todo
  S->>S: _TODOS.append(todo)
  S-->>R: Todo
  R->>R: todo.to_dict()
  R-)C: 딕셔너리 응답
  Note over R,C: 응답 직렬화는 FastAPI가 처리, 추적하지 않음
```

라우트가 시각을 만들고 저장소에 넘기면, 저장소가 모델에게 객체 생성을 맡기고 모델이 다시 저장소에서 id를 받아 오는 순환 호출이 일어납니다. FastAPI가 요청을 라우트 함수로 연결하고 반환값을 응답으로 바꾸는 부분은 읽지 않았습니다. 또한 `title`이 쿼리 파라미터로 전달된다는 점도 FastAPI의 기본 동작에 대한 추정입니다. <!-- codemap:unverified -->

1. `app/routes.py:create_todo` — `title.strip()`이 비었는지 검사
2. `app/utils.py:now_iso` — 현재 UTC 시각을 ISO 문자열로 반환
3. `app/storage.py:add_todo` — `Todo.create`를 호출해 객체를 만들고 `_TODOS`에 추가
4. `app/models.py:Todo.create` — `storage.next_id()`로 id를 받아 `Todo` 생성
5. `app/storage.py:next_id` — `len(_TODOS) + 1` 반환
6. `app/routes.py:create_todo` — `todo.to_dict()`를 반환

## GET /todos — 목록 조회

클라이언트가 `GET /todos`를 호출하면 `list_todos()`가 저장된 모든 할 일을 딕셔너리로 바꿔 돌려줍니다.

```mermaid
sequenceDiagram
  participant C as 클라이언트
  participant R as app/routes.py
  participant S as app/storage.py
  C-)R: GET /todos
  Note over C,R: FastAPI의 라우팅 호출은 추적하지 않음
  R->>S: all_todos()
  S-->>R: list(_TODOS) 복사본
  loop 각 할 일 t
    R->>R: t.to_dict()
  end
  R-)C: 딕셔너리 목록 응답
  Note over R,C: 응답 직렬화는 FastAPI가 처리, 추적하지 않음
```

저장소는 내부 리스트의 복사본만 돌려주므로 라우트가 원본을 바꾸지 않습니다. 프레임워크 구간은 위와 같이 추적하지 않았습니다. <!-- codemap:unverified -->

1. `app/routes.py:list_todos` — 저장소 목록 요청
2. `app/storage.py:all_todos` — `list(_TODOS)` 반환
3. `app/routes.py:list_todos` — 각 `Todo`에 `to_dict()` 호출

## POST /todos — 빈 제목 오류

제목이 공백뿐이면 저장소에 닿기 전에 422 오류로 끝납니다.

```mermaid
sequenceDiagram
  participant C as 클라이언트
  participant R as app/routes.py
  C-)R: POST /todos (공백 제목)
  Note over C,R: FastAPI의 라우팅 호출은 추적하지 않음
  alt title.strip()이 비어 있음
    R->>R: HTTPException(422, "title required") 발생
    R-)C: 422 오류 응답
    Note over R,C: 예외를 응답으로 바꾸는 일은 FastAPI가 처리, 추적하지 않음
  end
```

이 경로에서는 `app/utils.py`, `app/storage.py`, `app/models.py`가 호출되지 않습니다. 예외 처리는 프레임워크 동작이라 읽지 않았습니다. <!-- codemap:unverified -->

1. `app/routes.py:create_todo` — 조건 `not title.strip()`이 참이면 `HTTPException(status_code=422, detail="title required")`를 발생

## 다루지 않은 범위

`app/routes.py`, `app/storage.py`, `app/models.py`, `app/utils.py`, `app/main.py`를 읽었습니다. FastAPI 내부(라우팅, 직렬화, 예외 처리)는 라이브러리 코드라 읽지 않았습니다.
