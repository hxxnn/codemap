---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 마인드맵

`todo-api` 프로젝트를 기능 단위로 한눈에 보는 지도입니다.

```mermaid
mindmap
  root((todo-api))
    a1["진입점"]
      a2["app/main.py: FastAPI 앱 생성"]
    a3["API"]
      a4["app/routes.py: HTTP 라우트"]
        a5["create_todo()"]
        a6["list_todos()"]
    a7["도메인 모델"]
      a8["app/models.py: Todo 데이터클래스"]
        a9["Todo.create()"]
    a10["저장소"]
      a11["app/storage.py: 메모리 저장"]
        a12["add_todo()"]
        a13["all_todos()"]
    a14["유틸리티"]
      a15["app/utils.py: 시각 헬퍼"]
        a16["now_iso()"]
    a17["설정과 문서"]
      a18["pyproject.toml: 의존성"]
      a19["README.md: 실행 방법"]
```

모든 파일이 `app/` 패키지 아래 다섯 개의 역할로 나뉘고, 설정과 문서가 그 바깥에 있다는 것을 보여 줍니다.

## 그룹

- 진입점: `app/main.py`가 `FastAPI` 앱을 만들고 라우터를 등록합니다.
- API: `app/routes.py`의 `POST /todos`, `GET /todos`.
- 도메인 모델: `app/models.py`의 `Todo`(필드 `id`, `title`, `created_at`, `done`).
- 저장소: `app/storage.py`의 메모리 리스트 `_TODOS`. 생략한 항목: `next_id()`.
- 유틸리티: `app/utils.py`의 `now_iso()`.
- 설정과 문서: `pyproject.toml`(`fastapi`, `uvicorn` 의존성), `README.md`. 비어 있는 `app/__init__.py`는 지도에서 뺐습니다.

## 다루지 않은 범위

모든 소스 파일을 읽었으며 생략한 것은 위에 적은 `next_id()`와 비어 있는 `app/__init__.py`뿐입니다.
