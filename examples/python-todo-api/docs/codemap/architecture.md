---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, app/__init__.py: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 아키텍처 개요

`todo-api`는 FastAPI로 만든 작은 할 일 관리 서비스입니다. 아래에서 시스템 맥락, 컨테이너, 컴포넌트 순서로 확대해 가며 구조를 보여 줍니다.

## 1. 시스템 맥락

```mermaid
flowchart LR
  n1["사용자 / HTTP 클라이언트"]:::external
  n2["todo-api (app/)"]
  n1 -->|"HTTP 요청"| n2
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

사용자(HTTP 클라이언트)가 `todo-api`에 요청을 보내는 구조이며, 코드에서 확인된 외부 시스템은 없습니다(데이터베이스나 외부 API 호출 없음).

## 2. 컨테이너

```mermaid
flowchart LR
  n1["HTTP 클라이언트"]:::external
  n2["uvicorn 서버 (uvicorn app.main:app)"]
  n3["FastAPI 앱 (app/)"]
  n4["메모리 목록 _TODOS (app/storage.py)"]
  n1 -->|"HTTP"| n2
  n2 -->|"ASGI 앱 호출"| n3
  n3 -->|"함수 호출"| n4
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

실행은 `README.md`에 적힌 `uvicorn app.main:app` 한 프로세스이고, 데이터는 별도 DB 없이 같은 프로세스의 모듈 전역 리스트에만 보관됩니다.

## 3. 컴포넌트 (FastAPI 앱 내부)

```mermaid
flowchart LR
  n0["HTTP 클라이언트"]:::external
  subgraph entry["진입"]
    main["main (app/main.py)"]
  end
  subgraph api["API 층"]
    routes["routes (app/routes.py)"]
    utils["utils (app/utils.py)"]
  end
  subgraph data["데이터 층"]
    storage["storage (app/storage.py)"]
    models["models (app/models.py)"]
  end
  n0 -->|"요청"| main
  main -->|"include_router"| routes
  routes -->|"now_iso()"| utils
  routes -->|"add_todo, all_todos"| storage
  storage -->|"Todo.create"| models
  models -->|"next_id"| storage
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

`app/main.py`가 앱을 만들어 `app/routes.py`의 라우터를 붙이고, 라우트는 `app/storage.py`와 `app/utils.py`를 부릅니다. `app/storage.py`와 `app/models.py`는 서로를 import하는 순환 관계이며 코드 주석이 "deliberate cycle"이라고 적고 있습니다(자세한 내용은 `dependency-graph.md`).

## 다루지 않은 범위

저장소의 소스 파일 `app/main.py`, `app/routes.py`, `app/storage.py`, `app/models.py`, `app/utils.py`와 `README.md`, `pyproject.toml`을 모두 읽었습니다. `app/__init__.py`는 비어 있습니다. 읽지 않은 범위는 없습니다.
