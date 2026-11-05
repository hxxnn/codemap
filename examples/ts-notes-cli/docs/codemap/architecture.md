---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {README.md: ad3e9d59c7f90caab58f57655039b71b09108d4876e83a62570fdae41ee77e70, package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, tsconfig.json: fbfb5e54f48dbca20aff45f6530b732e22d3c4fd596d106e199b9ee5ff9eb439, src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 아키텍처 개요

`notes-cli`는 터미널에서 메모를 추가하고 목록을 보는 작은 TypeScript 명령줄 도구이며, 아래에서 세 단계의 확대 수준으로 구조를 보여 줍니다.

## 1단계: 시스템 컨텍스트

```mermaid
flowchart LR
  user["사용자 (터미널)"]:::external
  cli["notes-cli (src/index.ts)"]
  env["환경 변수 USER (process.env)"]:::external
  user -->|"notes add / list"| cli
  cli -->|"결과 / 오류 출력"| user
  cli -->|"USER 읽기"| env
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

사용자가 터미널에서 `notes add`나 `notes list`를 실행하고, 도구는 작성자 이름을 얻기 위해 환경 변수 `USER`를 읽습니다(`src/user-profile.ts`). 데이터베이스나 네트워크 API 호출은 코드에서 찾지 못했습니다.

## 2단계: 컨테이너

```mermaid
flowchart LR
  user["사용자 (터미널)"]:::external
  subgraph proc["Node.js 프로세스 (TypeScript, src/)"]
    entry["CLI 진입점 (src/index.ts)"]
    mem["메모 저장소: 메모리 배열 (src/notes-store.ts)"]
  end
  env["환경 변수 USER"]:::external
  user -->|"명령 인자"| entry
  entry -->|"추가 / 조회"| mem
  entry -->|"작성자 조회"| env
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

배포 단위는 하나의 CLI 프로세스뿐이며, 메모는 이 프로세스 안의 배열(`const notes: Note[] = []`)에만 저장되어 프로세스가 끝나면 사라집니다. `package.json`의 `bin`은 `notes`를 빌드 산출물 dist/index.js로 연결하고, `npm run build`는 `tsc`를 실행합니다.

## 3단계: 컴포넌트

```mermaid
flowchart LR
  subgraph entryl["진입 계층"]
    index["CLI 진입점 (src/index.ts)"]
  end
  subgraph domain["메모 도메인"]
    store["메모 저장소 (src/notes-store.ts)"]
    fmt["표시 포맷터 (src/format.ts)"]
    types["Note 타입 (src/types.ts)"]
  end
  subgraph envl["환경 계층"]
    prof["사용자 정보 (src/user-profile.ts)"]
  end
  env["환경 변수 USER"]:::external
  index -->|"addNote / listNotes"| store
  index -->|"currentUser"| prof
  store -->|"formatNote"| fmt
  store -.->|"Note"| types
  fmt -.->|"Note"| types
  prof -->|"읽기"| env
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

`src/index.ts`가 명령을 해석해 `src/notes-store.ts`와 `src/user-profile.ts`를 호출하고, 저장소는 `src/format.ts`로 한 줄 문자열을 만들며, 점선은 타입만 가져오는 의존입니다.

| 컴포넌트 | 책임 |
|---|---|
| `src/index.ts` | `process.argv`를 읽어 `add` / `list` / 사용법 오류로 분기 |
| `src/notes-store.ts` | 메모리 배열에 메모 추가(`addNote`), 포맷된 줄 목록 반환(`listNotes`) |
| `src/format.ts` | `#id 본문 (작성자)` 형식의 문자열 생성(`formatNote`) |
| `src/user-profile.ts` | `USER` 환경 변수 또는 `"anonymous"` 반환(`currentUser`) |
| `src/types.ts` | `Note` 인터페이스(`id`, `text`, `author`) 정의 |

## 다루지 않은 범위

소스 파일 5개(`src/` 전체)와 `README.md`, `package.json`, `tsconfig.json`을 모두 읽었습니다. 빌드 산출물 dist/와 node_modules/는 저장소에 없어 읽지 않았습니다.
