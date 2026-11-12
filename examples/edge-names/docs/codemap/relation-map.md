---
codemap: 1
skill: relation-map
generated_at: 2026-11-12
commit: null
sources: {package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 파일 관계 지도

소스 파일 3개가 서로 어떻게 `require`로 연결되는지, 각 파일이 쓰는 파일과 쓰이는 파일을 보여 줍니다.

## 파일 표

| 파일 | 한 줄 역할 | 쓰는 파일 | 쓰이는 파일 |
|---|---|---|---|
| `src/main.js` | 항목을 불러와 대문자로 바꿔 출력하는 시작 파일 | `src/my utils.js`, `src/데이터 로더.js` | — |
| `src/my utils.js` | 문자열을 대문자로 바꾸고 느낌표를 붙이는 함수 제공 | — | `src/main.js` |
| `src/데이터 로더.js` | 고정된 항목 목록의 복사본을 돌려주는 함수 제공 | — | `src/main.js` |

## 많이 쓰이는 파일

- `src/my utils.js` — 1곳에서 사용 (`src/main.js`)
- `src/데이터 로더.js` — 1곳에서 사용 (`src/main.js`)

## 순환 의존

순환 의존은 발견되지 않았습니다. 모든 연결이 `src/main.js`에서 나머지 두 파일로 한 방향으로만 이어집니다.

## 다루지 않은 범위

- 소스 파일 3개(`src/main.js`, `src/my utils.js`, `src/데이터 로더.js`)와 `package.json`을 전부 읽었습니다. 테스트 파일은 없습니다.
- 동적 import, 리플렉션, 런타임 플러그인 로딩은 코드에서 발견되지 않았습니다.
