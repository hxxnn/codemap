---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, docs/codemap/architecture.md: 2b6e167c9dbedd0a0a991cf4e28f06881effec8dc577b4eabbc9f3dd2f7c1d1b, docs/codemap/dependency-graph.md: 1ff1185b6bffd4380a275a913a259c61fca389f002db3f100ff830f739f6b7aa, docs/codemap/mindmap.md: 459515c471fd6eeecdb20c86e55c779a433ef6337ca462d52ec171b9d1c7b1ed, docs/codemap/sequence-flow.md: b2c4b40ae612a899265e544bb541e29722153ea53bc4dbee55ef7ee09e5b5ece}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 설계 문서와 온보딩 가이드

`todo-api`가 어떻게 만들어졌는지 설명하고, 처음 읽는 사람을 위한 코드 읽기 순서를 안내합니다.

## 개요

`todo-api`는 할 일을 만들고 목록으로 조회하는 아주 작은 REST 서비스입니다(`README.md`). Python과 FastAPI로 작성되었고 `uvicorn app.main:app`으로 실행합니다. 의존성은 `pyproject.toml`의 `fastapi>=0.110`, `uvicorn>=0.29` 두 가지입니다. 제공하는 기능은 `POST /todos`와 `GET /todos` 두 가지입니다.

## 구조

모든 코드는 `app/` 패키지의 다섯 모듈에 들어 있습니다. 진입점 `app/main.py`가 앱을 만들고, `app/routes.py`가 HTTP 요청을 받아, `app/storage.py`(메모리 저장)와 `app/models.py`(`Todo`), `app/utils.py`(시각 헬퍼)를 호출합니다. 계층별 그림은 `architecture.md`, import 관계와 순환은 `dependency-graph.md`, 기능별 요약은 `mindmap.md`, 실행 순서는 `sequence-flow.md`에 있습니다.

## 핵심 설계 선택

1. **메모리 안의 저장소 모듈**: 데이터를 `app/storage.py`의 모듈 전역 리스트 `_TODOS`에 보관합니다. 효과는 서버를 다시 시작하면 데이터가 사라진다는 것입니다. 이렇게 한 이유는 코드에 적혀 있지 않습니다. (추정: 예제 규모라서 단순함을 택했을 것) <!-- codemap:unverified -->
2. **라우터 분리**: `app/routes.py`의 `APIRouter`를 `app/main.py`에서 `include_router`로 붙입니다. 앱 생성과 엔드포인트 정의가 분리됩니다.
3. **의도된 순환 import**: `app/models.py`와 `app/storage.py`가 서로를 import합니다. 두 파일의 주석이 "deliberate cycle"이라고 밝히고 있어 의도된 선택이지만, 그 이유는 적혀 있지 않습니다. 효과로는 모델이 `storage.next_id()`로 id를 받고 저장소가 `models.Todo.create`로 객체를 만드는 양방향 호출이 생깁니다.
4. **모델 안의 직렬화**: `Todo.to_dict()`가 응답용 dict를 만들고, 라우트는 이를 그대로 반환합니다(`app/models.py`, `app/routes.py`).
5. **입력 검증은 라우트에서**: 제목이 공백이면 `app/routes.py`의 `create_todo`가 `HTTPException(422)`를 발생시킵니다.
6. **id는 리스트 길이로 계산**: `app/storage.py`의 `next_id()`는 `len(_TODOS) + 1`입니다. 항목을 삭제하는 기능이 생기면 id가 겹칠 수 있습니다(추정). <!-- codemap:unverified -->

## 읽는 순서

1. `README.md`: 프로젝트 목적과 실행 명령을 확인합니다.
2. `pyproject.toml`: 쓰는 외부 라이브러리를 확인합니다.
3. `app/main.py`: 앱이 만들어지고 라우터가 붙는 지점입니다.
4. `app/routes.py`: 실제 엔드포인트 두 개와 422 오류 처리를 봅니다.
5. `app/storage.py`: 데이터가 어디에 어떻게 저장되는지 봅니다.
6. `app/models.py`: `Todo` 필드와 `storage`로 되돌아오는 순환 호출을 봅니다.
7. `app/utils.py`: 마지막으로 시각 헬퍼 `now_iso`를 확인합니다.

## 다루지 않은 범위

`app/`의 모든 소스와 `pyproject.toml`, `README.md`를 읽었습니다. 테스트와 배포 설정은 저장소에 없고, 서버를 실제로 실행해 보지는 않았습니다.
