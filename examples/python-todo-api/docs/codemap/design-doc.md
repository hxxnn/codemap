---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, docs/codemap/architecture.md: 6ea477d6b5bc1aef5643bdf338e664ff5355ed9404d62e92960b3ed91bc79af4, docs/codemap/dependency-graph.md: ac1d2a9685e73a401a99d37f0bbd0ba730a7953898109e771bb9223125fbc1db, docs/codemap/mindmap.md: 1e2492cfadd2cc14e820764aff9228f0091fb484fb210ddbd5eea5672235a38c, docs/codemap/sequence-flow.md: 247d923ea78f0be0a1d08d84b94aa1c659a680dc69b36c6f97ffe928eb7395cb}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 설계 문서와 온보딩 가이드

## 개요

`todo-api`는 할 일을 추가하고 목록으로 조회하는 작은 HTTP API입니다. Python과 FastAPI로 만들었고 `uvicorn app.main:app`으로 실행합니다(`README.md`, `pyproject.toml`의 의존성 `fastapi`, `uvicorn`). 데이터는 DB 없이 프로세스 메모리에만 보관합니다.

## 구조

요청은 `app/main.py`의 앱에서 `app/routes.py`의 두 라우트(`POST /todos`, `GET /todos`)로 들어가고, 라우트는 `app/storage.py`에 저장·조회를 맡기고 `app/utils.py`에서 시각을 받아 옵니다. `app/storage.py`는 `app/models.py`의 `Todo`로 객체를 만듭니다. 그림은 `architecture.md`, 파일별 import는 `dependency-graph.md`, 실행 순서는 `sequence-flow.md`, 파일·함수 목록은 `mindmap.md`에 있습니다.

## 핵심 설계 선택

1. **메모리 저장소를 작은 모듈 뒤에 둠** — `app/storage.py`의 모듈 전역 `_TODOS` 리스트를 `add_todo()`, `all_todos()`, `next_id()` 함수로만 다룹니다. 효과: 라우트는 저장 방식을 모르지만, 재시작하면 데이터가 사라집니다. 이렇게 한 이유는 코드에 적혀 있지 않습니다 (추정: 단순한 예제라서) <!-- codemap:unverified -->
2. **저장소와 모델의 의도적 순환 import** — `app/storage.py`와 `app/models.py`가 서로를 import하며, 두 파일 모두 주석에 "deliberate cycle"이라고 적혀 있습니다. 효과: `Todo.create()`가 `storage.next_id()`로 id를 받고, 저장소는 `models.Todo.create()`로 객체를 만드는 양방향 호출이 생깁니다. 의도적이라는 사실만 주석에 있고 이유는 없습니다 (확인 필요) <!-- codemap:unverified -->
3. **리소스 하나에 라우터 하나** — `app/routes.py`가 `APIRouter`를 만들고 `app/main.py`가 `include_router`로 붙입니다. 효과: 라우트가 늘어도 `app/main.py`는 거의 변하지 않습니다.
4. **검증은 라우트 함수에서** — `create_todo()`가 공백뿐인 제목이면 `HTTPException(422)`를 던집니다. 효과: 모델과 저장소는 이미 검증된 입력만 받습니다.
5. **데이터클래스 모델과 `to_dict()`** — `app/models.py`의 `Todo`는 `@dataclass`이고 응답용 변환 메서드를 직접 가집니다. 효과: 응답 모양이 한 곳에 모입니다.

## 읽는 순서

1. `README.md` — 서비스가 무엇이고 어떻게 실행하는지 확인
2. `pyproject.toml` — 의존성이 `fastapi`와 `uvicorn`뿐임을 확인
3. `app/main.py` — 진입점. 앱 생성과 라우터 등록만 있음
4. `app/routes.py` — 핵심 흐름. 두 라우트가 저장소를 어떻게 부르는지 확인
5. `app/storage.py` — 메모리 목록과 id 부여 방식(`len(_TODOS) + 1`)
6. `app/models.py` — `Todo` 정의와, 저장소와의 순환 import 확인
7. `app/utils.py` — 마지막으로 `now_iso()` 하나뿐인 보조 함수

## 다루지 않은 범위

소스 파일 6개와 `README.md`, `pyproject.toml`을 모두 읽었고 빠뜨린 범위는 없습니다. FastAPI와 uvicorn 내부 동작, 테스트(저장소에 없음)는 다루지 않았습니다.
