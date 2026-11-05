---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 의존성 그래프

각 파일의 `require` 구문을 직접 읽어 만든 그래프이며, 화살표는 가져오는 쪽에서 가져와지는 쪽을 향합니다.

```mermaid
flowchart LR
  n1["src/main.js"]
  n2["src/my utils.js"]
  n3["src/데이터 로더.js"]
  n1 --> n2
  n1 --> n3
```

`src/main.js`만 다른 파일 두 개를 가져오고, 나머지 두 파일은 아무것도 가져오지 않습니다.

## 순환 의존

순환 의존은 발견되지 않았습니다. 세 파일의 의존 방향은 `src/main.js`에서 나가는 한 방향뿐입니다.

## 가장 많이 의존되는 파일

- `src/my utils.js`: `src/main.js`가 1번 가져옵니다.
- `src/데이터 로더.js`: `src/main.js`가 1번 가져옵니다.

## 다루지 않은 범위

소스 파일 3개를 모두 읽었고 외부 패키지 import는 없었습니다. 동적 `require`도 없어서 추적하지 못한 의존은 없습니다.
