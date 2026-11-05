---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 아키텍처 개요

`edge-names`는 항목 목록을 불러와 대문자로 바꾼 뒤 터미널에 출력하는 아주 작은 Node.js 프로그램이며, 아래에 세 단계의 확대 수준으로 구조를 보여 줍니다.

## 1단계: 시스템 컨텍스트

```mermaid
flowchart LR
  user["실행하는 사용자"]:::external
  sys["edge-names (Node.js 프로그램)"]
  out["표준 출력 (터미널)"]:::external
  user -->|"node 실행"| sys
  sys -->|"console.log"| out
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

사용자가 `src/main.js`를 실행하면 프로그램이 결과 줄을 표준 출력으로 내보냅니다.

## 2단계: 컨테이너

```mermaid
flowchart LR
  user["실행하는 사용자"]:::external
  subgraph proc["단일 Node.js 프로세스"]
    cli["CLI 스크립트 (JavaScript, src/)"]
  end
  out["표준 출력 (터미널)"]:::external
  user -->|"실행"| cli
  cli -->|"줄 출력"| out
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

배포 단위는 `src/` 폴더의 스크립트 하나뿐이며, 서버·데이터베이스·네트워크 호출은 코드에서 찾지 못했습니다.

## 3단계: 컴포넌트

```mermaid
flowchart LR
  subgraph app["src/ (CLI 컨테이너)"]
    main["진입점 (src/main.js)"]
    utils["문자열 변환 (src/my utils.js)"]
    loader["데이터 로더 (src/데이터 로더.js)"]
  end
  out["표준 출력 (터미널)"]:::external
  main -->|"loadItems()"| loader
  main -->|"shout()"| utils
  main -->|"console.log"| out
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

`src/main.js`가 `src/데이터 로더.js`에서 항목을 받고, 각 항목을 `src/my utils.js`의 `shout()`로 변환해 출력합니다. `src/데이터 로더.js`는 모듈 안의 고정 배열(`alpha`, `beta`, `gamma`)을 복사해 돌려줍니다.

## 다루지 않은 범위

소스 파일 3개(`src/main.js`, `src/my utils.js`, `src/데이터 로더.js`)와 `package.json`을 모두 읽었으며, 읽지 않은 범위는 없습니다.
