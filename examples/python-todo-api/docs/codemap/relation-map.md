---
codemap: 1
skill: relation-map
generated_at: 2026-11-12
commit: null
sources: {app/__init__.py: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, app/main.py: 137eaf99210854cdae4594b10f7650a868c121c96343a0136e8ddeb5c820b625, app/models.py: 810e4e46c5f327af8853fab85132e666b70e9550cf5b12f4ae28aad84f1ba091, app/routes.py: 377631c48b9b9be27f99f9d510d77e1f182a633f2a63605686d201ea5479ddce, app/storage.py: 774e6947a67eea390b5fd6cef912293c3e2ffd94e7c2377f2b9c07f79c578a89, app/utils.py: aa17c15daf74a9a7d6affdb3292a2478d2b9a3886277593917f765c783d3ca66, pyproject.toml: d39952121dd8849656d105526fe1915af998c94fe648b6a7e32a214e53ac420d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 파일 관계 지도

`app/` 폴더의 파이썬 파일 6개가 서로 어떤 파일을 가져다 쓰는지(import)를 코드에서 읽은 그대로 보여 줍니다.

## 파일 표

| 파일 | 역할 | 쓰는 파일 | 쓰이는 파일 |
|---|---|---|---|
| `app/__init__.py` | app 패키지를 표시하는 빈 파일 | — | — |
| `app/main.py` | FastAPI 앱을 만들고 라우터를 연결함 | `app/routes.py` | — |
| `app/models.py` | Todo 데이터 클래스와 생성 함수를 정의함 | `app/storage.py` | `app/storage.py` |
| `app/routes.py` | 할 일 추가와 목록 조회 API 경로를 처리함 | `app/storage.py`, `app/utils.py` | `app/main.py` |
| `app/storage.py` | 메모리 목록에 할 일을 저장하고 꺼냄 | `app/models.py` | `app/models.py`, `app/routes.py` |
| `app/utils.py` | 현재 시각을 ISO 문자열로 돌려줌 | — | `app/routes.py` |

## 많이 쓰이는 파일

- `app/storage.py` — 2곳에서 씀 (`app/models.py`, `app/routes.py`)
- `app/models.py` — 1곳에서 씀 (`app/storage.py`)
- `app/routes.py` — 1곳에서 씀 (`app/main.py`)
- `app/utils.py` — 1곳에서 씀 (`app/routes.py`)

## 순환 의존

파일 2개로 이루어진 순환 하나가 있습니다: `app/models.py` 와 `app/storage.py` 가 서로를 가져옵니다.

- 예: `app/models.py` → `app/storage.py` → `app/models.py`

두 파일 모두 코드 주석에 의도한 순환이라고 적혀 있습니다.

## 다루지 않은 범위

- `app/` 아래 파이썬 파일 6개와 `pyproject.toml` 을 모두 읽었습니다. 소스 폴더는 이게 전부입니다.
- 테스트 파일은 저장소에 없어 표에 넣지 않았습니다.
- 동적 import, 리플렉션, 런타임 플러그인 로딩은 코드에서 찾지 못했습니다.
- `from app import storage` 는 패키지 `app` 도 함께 불러오지만, `app/__init__.py` 가 비어 있어 선은 그리지 않았습니다.
- 외부 패키지(`fastapi`, `dataclasses`, `datetime`)는 프로젝트 안의 파일이 아니라서 뺐습니다.
