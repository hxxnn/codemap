---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {README.md: 0400cdfb761e16937066332c0598879036142b20ef8fbf1835531feb33087731, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d, app/__init__.py: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 구조 트리

`todo-api`의 기능과 파일, 주요 함수를 한 장의 트리로 정리했습니다.

- **todo-api** — 할 일을 추가하고 목록으로 보여 주는 작은 FastAPI 서비스
  - **진입** — 앱을 만들고 라우터를 붙이는 곳
    - `app/main.py` — `FastAPI` 앱 생성과 라우터 등록
  - **API** — HTTP 요청을 받는 층
    - `app/routes.py` — POST·GET `/todos` 라우트
      - `create_todo()` — 제목을 검사하고 저장소에 넘김
      - `list_todos()` — 저장된 할 일을 딕셔너리 목록으로 반환
  - **저장소** — 메모리에 보관
    - `app/storage.py` — 모듈 전역 목록 `_TODOS`
      - `add_todo()` — 할 일을 만들어 목록에 추가
      - `all_todos()` — 목록의 복사본 반환
      - `next_id()` — 다음 id 계산
  - **모델** — 할 일 데이터 형태
    - `app/models.py` — `Todo` 데이터클래스
      - `Todo.create()` — 저장소에서 id를 받아 `Todo` 생성
      - `Todo.to_dict()` — 응답용 딕셔너리로 변환
  - **유틸** — 공용 보조 함수
    - `app/utils.py` — 시간 문자열 생성
      - `now_iso()` — 현재 UTC 시각을 ISO 문자열로 반환

## 그룹별 설명

- **진입**: `uvicorn app.main:app`으로 시작하는 유일한 진입점입니다. 빈 파일 `app/__init__.py`는 트리에서 뺐습니다.
- **API**: 입력 검증(빈 제목이면 422)과 응답 변환을 맡습니다.
- **저장소**: DB 없이 프로세스 메모리에만 저장하므로 재시작하면 데이터가 사라집니다.
- **모델**: `app/storage.py`와 서로 import하는 순환 관계입니다(`dependency-graph.md` 참고).
- **유틸**: 함수가 하나뿐입니다.

## 다루지 않은 범위

소스 파일 6개와 `README.md`, `pyproject.toml`을 모두 읽었습니다. 읽지 않은 범위는 없습니다.
