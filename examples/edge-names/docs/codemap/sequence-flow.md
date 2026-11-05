---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 시퀀스 흐름

프로그램에는 실행 경로가 하나뿐이어서 시나리오를 하나만 골랐습니다. 분기나 오류 처리 코드가 없어 다른 시나리오는 만들지 않았습니다.

## 프로그램 실행: 항목을 대문자로 출력

사용자가 `src/main.js`를 실행하면 시작됩니다.

```mermaid
sequenceDiagram
  actor U as 사용자
  participant M as src/main.js
  participant L as src/데이터 로더.js
  participant S as src/my utils.js
  participant O as 표준 출력
  U->>M: node 실행
  M->>L: loadItems()
  L-->>M: 배열 복사본 (alpha, beta, gamma)
  loop 항목마다
    M->>S: shout(item)
    S-->>M: 대문자 + 느낌표
    M->>O: console.log(결과)
  end
```

1. 시작 시 `src/main.js`가 `require`로 두 모듈을 불러옵니다 (`src/main.js:shout`, `src/main.js:loadItems`).
2. `src/main.js`가 `loadItems()`를 호출하고, `src/데이터 로더.js:loadItems`가 내부 배열의 `slice()` 복사본을 돌려줍니다.
3. `for...of` 반복에서 각 항목마다 `src/my utils.js:shout`를 호출해 `toUpperCase()`에 `"!"`를 붙인 문자열을 받습니다.
4. 받은 문자열을 `src/main.js`가 `console.log`로 출력합니다. 결과는 `ALPHA!`, `BETA!`, `GAMMA!` 순서입니다.

## 다루지 않은 범위

소스 파일 3개를 모두 읽었으며, 읽지 않은 범위는 없습니다. 추적하지 못한 호출도 없습니다.
