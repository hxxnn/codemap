---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62, package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 아키텍처 개요

`notes-cli`는 터미널에서 메모를 추가하고 목록으로 보는 작은 TypeScript 명령줄 도구이며, 아래에 세 단계의 확대 수준으로 구조를 그렸습니다.

## 1. 시스템 컨텍스트

```mermaid
flowchart LR
  user["터미널 사용자"]:::external
  env["환경변수 USER"]:::external
  sys["notes-cli (CLI 도구)"]
  user -->|"notes add / list"| sys
  env -->|"작성자 이름"| sys
  sys -->|"메모 출력"| user
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

사용자가 `notes` 명령을 실행하면 도구가 환경변수 `USER`에서 작성자 이름을 읽고 결과를 터미널에 출력합니다(`src/index.ts`, `src/user-profile.ts`).

## 2. 컨테이너

```mermaid
flowchart LR
  user["터미널 사용자"]:::external
  subgraph proc["notes 프로세스 (Node.js, src/)"]
    cli["CLI 프로세스 (TypeScript, src/)"]
    mem["메모리 내 notes 배열 (src/notes-store.ts)"]
  end
  user -->|"명령 실행"| cli
  cli -->|"읽기/쓰기"| mem
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

배포 단위는 `package.json`의 `bin`이 가리키는 단일 CLI 하나이고, 저장소는 별도 DB 없이 프로세스 메모리의 배열뿐이라 명령이 끝나면 메모는 사라집니다.

## 3. 컴포넌트

```mermaid
flowchart LR
  subgraph entry["진입"]
    idx["CLI 진입 (src/index.ts)"]
  end
  subgraph logic["로직"]
    store["메모 저장소 (src/notes-store.ts)"]
    prof["사용자 정보 (src/user-profile.ts)"]
    fmt["포맷터 (src/format.ts)"]
  end
  subgraph shared["공유"]
    types["타입 (src/types.ts)"]
  end
  idx -->|"addNote, listNotes"| store
  idx -->|"currentUser"| prof
  store -->|"formatNote"| fmt
  store -->|"Note"| types
  fmt -->|"Note"| types
```

`src/index.ts`가 명령을 해석해 저장소와 사용자 정보 모듈을 부르고, 저장소는 출력 문자열 생성을 `src/format.ts`에 맡기며, `Note` 타입은 `src/types.ts` 한 곳에 정의됩니다.

## 다루지 않은 범위

`tsconfig.json`은 읽지 않았고, 빌드 산출물 `dist/`는 저장소에 없어 보지 못했습니다. 나머지 소스 5개는 모두 끝까지 읽었습니다.
