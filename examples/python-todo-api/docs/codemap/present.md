---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 6ea477d6b5bc1aef5643bdf338e664ff5355ed9404d62e92960b3ed91bc79af4, docs/codemap/dependency-graph.md: ac1d2a9685e73a401a99d37f0bbd0ba730a7953898109e771bb9223125fbc1db, docs/codemap/mindmap.md: 1e2492cfadd2cc14e820764aff9228f0091fb484fb210ddbd5eea5672235a38c, docs/codemap/sequence-flow.md: 247d923ea78f0be0a1d08d84b94aa1c659a680dc69b36c6f97ffe928eb7395cb, docs/codemap/design-doc.md: 6dd86e01f24f0b35b939aeec00fba0f3d7970868719dc9b3ec08e6a79835c4ea}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 발표 개요

`todo-api` 코드베이스를 팀에 소개하기 위한 7장짜리 개요입니다. 다섯 개 문서가 모두 있어 빠진 슬라이드는 없습니다.

## 슬라이드 1: 이게 무엇인가

할 일을 추가하고 목록으로 조회하는 작은 HTTP API이고, Python과 FastAPI로 만들어 `uvicorn app.main:app`으로 실행합니다. 데이터는 DB 없이 메모리에만 보관합니다.
Show: `design-doc.md` → "개요"

## 슬라이드 2: 전체 그림

사용자 요청은 uvicorn을 거쳐 FastAPI 앱으로 들어가고, 앱 안의 메모리 목록에 저장됩니다. 외부 시스템은 없습니다.
Show: `architecture.md` → "2. 컨테이너" 다이어그램

## 슬라이드 3: 어떻게 구성되어 있나

진입, API, 저장소, 모델, 유틸의 다섯 그룹이고 파일은 `app/` 아래 5개입니다.
Show: `mindmap.md` → "구조 트리"

## 슬라이드 4: 어떻게 실행되나

`POST /todos`는 라우트가 시각을 만들고, 저장소가 모델에게 객체 생성을 맡기는 순서로 흐릅니다. FastAPI가 처리하는 구간은 추적하지 않았습니다. <!-- codemap:unverified -->
Show: `sequence-flow.md` → "POST /todos — 할 일 추가" 다이어그램

## 슬라이드 5: 부품끼리의 의존 관계

대부분 한 방향 흐름이지만 `app/storage.py`와 `app/models.py`가 서로를 import하는 순환이 하나 있고, 코드 주석이 의도적이라고 밝힙니다.
Show: `dependency-graph.md` → 의존성 그래프 다이어그램과 "순환 의존"

## 슬라이드 6: 핵심 설계 선택

메모리 저장소를 작은 모듈 뒤에 두었고, 저장소와 모델은 의도적으로 순환 import합니다. 이렇게 한 이유는 코드에 없습니다 (추정) <!-- codemap:unverified -->
Show: `design-doc.md` → "핵심 설계 선택"

## 슬라이드 7: 어디서부터 읽을까

`README.md`, `pyproject.toml`, `app/main.py`, `app/routes.py` 순으로 읽으면 전체 흐름이 잡힙니다.
Show: `design-doc.md` → "읽는 순서"

## 다루지 않은 범위

소스 파일과 설정 파일은 모두 읽었고 빠진 범위는 없습니다. FastAPI와 uvicorn 내부 동작은 다루지 않았습니다.
