---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 2b6e167c9dbedd0a0a991cf4e28f06881effec8dc577b4eabbc9f3dd2f7c1d1b, docs/codemap/dependency-graph.md: 1ff1185b6bffd4380a275a913a259c61fca389f002db3f100ff830f739f6b7aa, docs/codemap/mindmap.md: 459515c471fd6eeecdb20c86e55c779a433ef6337ca462d52ec171b9d1c7b1ed, docs/codemap/sequence-flow.md: b2c4b40ae612a899265e544bb541e29722153ea53bc4dbee55ef7ee09e5b5ece, docs/codemap/design-doc.md: 224526f05301415f2712d9b9c73f967995e6ab5f00d80e57bdd5fcdea38fefbd}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 발표 개요: todo-api

`todo-api` 코드베이스를 팀에 소개하기 위한 7장짜리 슬라이드 구성안입니다.

## 슬라이드 1: 이 프로젝트는 무엇인가

할 일을 만들고 목록으로 조회하는 아주 작은 REST 서비스입니다. Python, FastAPI, uvicorn으로 만들어졌습니다.
Show: `design-doc.md` → "개요" 섹션

## 슬라이드 2: 큰 그림

HTTP 클라이언트가 하나의 uvicorn 프로세스에 요청하고, 데이터는 같은 프로세스의 메모리 리스트에 저장됩니다.
Show: `architecture.md` → "컨테이너" 다이어그램

## 슬라이드 3: 어떻게 구성되어 있나

`app/` 아래 진입점, API, 모델, 저장소, 유틸리티의 다섯 역할로 나뉩니다.
Show: `mindmap.md` → 마인드맵 다이어그램

## 슬라이드 4: 어떻게 실행되나

`POST /todos`는 시각 생성, 저장소 추가, 모델 생성, dict 변환 순서로 진행됩니다. 라우팅과 직렬화는 프레임워크 내부라 추적하지 않았습니다.
Show: `sequence-flow.md` → "POST /todos: 할 일 만들기" 다이어그램

## 슬라이드 5: 부분들의 의존 관계

`app/main.py`에서 `app/routes.py`를 거쳐 `app/storage.py`와 `app/utils.py`로 이어집니다. `app/models.py`와 `app/storage.py`는 서로를 import하는 순환 의존이며, 주석에 "deliberate cycle"로 적혀 있습니다.
Show: `dependency-graph.md` → 의존성 그래프 다이어그램

## 슬라이드 6: 핵심 설계 선택

- 메모리 안의 저장소 모듈(`app/storage.py`): 재시작하면 데이터가 사라집니다. 이유는 코드에 없습니다. (추정) <!-- codemap:unverified -->
- 라우터 분리: `app/routes.py`의 라우터를 `app/main.py`에서 붙입니다.
- 의도된 순환 import: `app/models.py`와 `app/storage.py`가 서로 호출합니다.

Show: `design-doc.md` → "핵심 설계 선택" 섹션

## 슬라이드 7: 어디서부터 읽을까

`README.md`, `pyproject.toml`, `app/main.py`, `app/routes.py`, `app/storage.py` 순서로 읽기 시작합니다.
Show: `design-doc.md` → "읽는 순서" 섹션

## 다루지 않은 범위

각 산출물의 "다루지 않은 범위"를 따릅니다. 모든 소스와 `README.md`, `pyproject.toml`을 읽었고, 테스트와 배포 설정은 저장소에 없으며, FastAPI 내부 동작과 실제 서버 실행은 확인하지 않았습니다.
