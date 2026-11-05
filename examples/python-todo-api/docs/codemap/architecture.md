---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 아키텍처 개요

`todo-api`는 FastAPI로 만든 작은 할 일(todo) REST 서비스이며, 아래에서 시스템 맥락, 컨테이너, 컴포넌트 순서로 세 단계로 확대해 설명합니다.

## 시스템 맥락

```mermaid
flowchart LR
  user["HTTP 클라이언트"]:::external
  sys["todo-api 서비스"]
  user -->|"HTTP 요청"| sys
  sys -->|"JSON 응답"| user
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

사용자(HTTP 클라이언트)가 `/todos` 경로로 요청을 보내고 JSON을 돌려받는 단일 시스템이며, 코드에서 확인된 외부 데이터베이스나 타사 API는 없습니다.

## 컨테이너

```mermaid
flowchart LR
  user["HTTP 클라이언트"]:::external
  subgraph proc["uvicorn 프로세스 (README.md)"]
    api["FastAPI 앱 (Python, app/)"]
    mem["메모리 목록 _TODOS (app/storage.py)"]
  end
  user -->|"HTTP"| api
  api -->|"함수 호출"| mem
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

배포 단위는 `uvicorn app.main:app`으로 실행되는 하나의 프로세스이고, 데이터는 별도 DB 없이 같은 프로세스의 파이썬 리스트에 저장됩니다.

## 컴포넌트

```mermaid
flowchart LR
  user["HTTP 클라이언트"]:::external
  subgraph app["app/ 패키지"]
    main["main (app/main.py)"]
    routes["routes (app/routes.py)"]
    models["models (app/models.py)"]
    storage["storage (app/storage.py)"]
    utils["utils (app/utils.py)"]
  end
  user -->|"HTTP"| main
  main -->|"include_router"| routes
  routes -->|"add_todo, all_todos"| storage
  routes -->|"now_iso"| utils
  storage -->|"Todo.create"| models
  models -->|"next_id"| storage
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

`app/main.py`가 `FastAPI` 앱을 만들어 `app/routes.py`의 라우터를 등록하고, 라우트는 `app/storage.py`와 `app/utils.py`를 호출하며, `app/storage.py`와 `app/models.py`는 서로를 호출합니다.

- `app/main.py`: `FastAPI(title="todo-api")` 생성과 `include_router(router)`.
- `app/routes.py`: `POST /todos`(`create_todo`)와 `GET /todos`(`list_todos`).
- `app/models.py`: `Todo` 데이터클래스(`to_dict`, `create`).
- `app/storage.py`: 모듈 전역 `_TODOS` 리스트와 `next_id`, `add_todo`, `all_todos`.
- `app/utils.py`: UTC 현재 시각을 ISO 문자열로 돌려주는 `now_iso`.

## 다루지 않은 범위

저장소의 소스 파일(`app/*.py`, 총 65줄)과 `pyproject.toml`, `README.md`를 모두 읽었습니다. 테스트, 배포 설정, 실제 실행은 저장소에 없거나 확인하지 않았습니다.
