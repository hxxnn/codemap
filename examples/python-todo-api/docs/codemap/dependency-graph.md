---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {app/__init__.py: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 의존성 그래프

각 파일의 import 문을 직접 읽어 "누가 누구를 가져오는가"를 화살표(importer → imported)로 그렸습니다. 서드파티 패키지(`fastapi`, `dataclasses`, `datetime`)는 제외했습니다.

```mermaid
flowchart LR
  storage["app/storage.py"]:::cycle
  models["app/models.py"]:::cycle
  main["app/main.py"]
  routes["app/routes.py"]
  utils["app/utils.py"]
  storage --> models
  models --> storage
  main --> routes
  routes --> storage
  routes --> utils
  linkStyle 0 stroke:#C62F3E,stroke-width:3px
  linkStyle 1 stroke:#C62F3E,stroke-width:3px
  classDef cycle fill:#FDECEE,stroke:#C62F3E,color:#7A1823
```

`app/storage.py`와 `app/models.py`가 서로를 가져오는 순환(빨간 화살표)이 있고, 나머지는 `app/main.py` → `app/routes.py` → 저장소/유틸 순의 한 방향 흐름입니다.

## 순환 의존

순환 그룹이 1개 있습니다.

- 파일: `app/storage.py`, `app/models.py`
- 예시 순환: `app/storage.py` → `app/models.py` → `app/storage.py`
- 근거: `app/storage.py`의 `from app import models`와 `app/models.py`의 `from app import storage`. 두 줄 모두 주석에 "deliberate cycle"이 적혀 있습니다.
- 두 import가 모듈 최상단에서 `from app import ...` 형태로 모듈 객체만 가져오고 사용은 함수 안에서 하므로, 실행 시점에는 동작하는 구조로 보입니다 (추정) <!-- codemap:unverified -->

## 가장 많이 import되는 파일

- `app/storage.py` — 2회 (`app/routes.py`, `app/models.py`)
- `app/models.py` — 1회 (`app/storage.py`)
- `app/routes.py` — 1회 (`app/main.py`)
- `app/utils.py` — 1회 (`app/routes.py`)

`app/__init__.py`는 비어 있어 import도 피import도 없습니다. 동적 import나 플러그인 로딩은 코드에서 발견되지 않았습니다.

## 다루지 않은 범위

`app/` 아래 파이썬 파일 6개를 모두 읽었습니다. 읽지 않은 범위는 없습니다.
