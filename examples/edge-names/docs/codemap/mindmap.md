---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 구조 트리

프로젝트를 기능 단위로 묶어 파일과 핵심 함수까지 한눈에 보여 주는 트리입니다.

- **edge-names** — 공백·한글 파일명을 가진 모듈들을 불러와 항목을 출력하는 작은 Node.js 프로그램
  - **진입점** — 실행이 시작되고 전체 흐름을 조립하는 곳
    - `src/main.js` — 두 모듈을 불러와 항목마다 출력
  - **문자열 가공** — 텍스트를 바꾸는 유틸리티
    - `src/my utils.js` — 문자열 유틸 모듈
      - `shout()` — 대문자로 바꾸고 느낌표를 붙임
  - **데이터** — 출력할 항목을 제공
    - `src/데이터 로더.js` — 항목 목록 모듈
      - `loadItems()` — 항목 배열의 복사본을 돌려줌

## 그룹별 설명

- **진입점** — `package.json`의 `main`이 가리키는 파일 하나뿐입니다.
- **문자열 가공** — 함수 하나만 내보내므로 트리에서 빠뜨린 항목은 없습니다.
- **데이터** — `alpha`, `beta`, `gamma` 세 항목이 모듈 안에 고정되어 있고, 빠뜨린 항목은 없습니다.

## 다루지 않은 범위

소스 3개를 모두 읽었습니다. `src/데이터 로더.js`는 경로에 한글이 있어 해시 안전 규칙을 통과하지 못해 `sources`에 넣지 못했습니다 (확인 필요) <!-- codemap:unverified -->.
