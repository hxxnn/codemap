---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62, package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, README.md: ad3e9d59c7f90caab58f57655039b71b09108d4876e83a62570fdae41ee77e70, docs/codemap/architecture.md: 0b3d1389317e9a0ab4fcb87446bf55dd34567826c9c1d89d3aa18a4811970932, docs/codemap/dependency-graph.md: aaa5364d6b569e97ed9c72dd055cca72632c28d218b04d52f7ab502ab70f0fd1, docs/codemap/mindmap.md: de0ef7d606a8d96be6c3780193bf9e99e1dcb2477c15b6e7a5935ef5e3981b3e, docs/codemap/sequence-flow.md: 015eee2d2ee144769340373a10396a28dcd96430248ba4df188439328af1efa9}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 설계 문서와 온보딩 가이드

## 개요

`notes-cli`는 `notes add "text"`로 메모를 추가하고 `notes list`로 보는 명령줄 메모 도구입니다(`README.md`). TypeScript로 작성되었고 `package.json`의 `bin`이 `notes`를 `dist/index.js`에 연결하며, 빌드는 `tsc`를 씁니다. 런타임 의존성은 없고 개발 의존성은 `typescript`뿐입니다.

## 구조

진입 파일 `src/index.ts`가 명령을 나누고, 저장소(`src/notes-store.ts`), 사용자 정보(`src/user-profile.ts`), 포맷터(`src/format.ts`), 타입(`src/types.ts`)이 각각 한 가지 일만 맡습니다. 세 단계 다이어그램은 `architecture.md`, import 관계는 `dependency-graph.md`, 파일별 트리는 `mindmap.md`, 호출 순서는 `sequence-flow.md`에 있습니다. 의존 방향은 한쪽으로만 흐르며 순환은 없습니다.

## 핵심 설계 선택

1. **메모리 내 저장소** — `src/notes-store.ts`의 모듈 전역 배열 `notes`에 보관합니다. 효과: 프로세스가 끝나면 메모가 사라지므로 `add` 뒤 `list`를 다른 실행에서 해도 비어 있습니다. 이유는 코드에 적혀 있지 않습니다. (추정: 프로토타입이라서) <!-- codemap:unverified -->
2. **진입 파일에서 명령 분기** — `src/index.ts` 한 파일에서 `process.argv`를 직접 `if/else`로 나눕니다. 효과: 명령이 둘뿐이라 단순하지만, 명령이 늘면 이 파일이 커집니다.
3. **출력 형식 분리** — `formatNote()`를 `src/format.ts`로 따로 두고 저장소가 `map(formatNote)`로 부릅니다. 효과: 출력 모양을 저장 로직과 독립해 바꿀 수 있습니다.
4. **작성자는 환경변수에서** — `currentUser()`가 `process.env.USER ?? "anonymous"`를 반환합니다(`src/user-profile.ts`). 효과: 로그인 개념 없이 OS 사용자 이름을 씁니다.
5. **타입 한 곳 정의** — `Note` 인터페이스를 `src/types.ts`에만 두어 저장소와 포맷터가 함께 씁니다.

## 읽는 순서

1. `README.md` — 도구의 목적과 사용법을 먼저 확인합니다.
2. `package.json` — `bin`과 빌드 스크립트로 실행 방식을 봅니다.
3. `src/index.ts` — 실행이 시작되는 곳이며 `add`/`list` 분기를 봅니다.
4. `src/notes-store.ts` — 메모가 어디에 어떻게 쌓이는지 봅니다.
5. `src/format.ts` — 출력 한 줄의 모양을 확인합니다.
6. `src/types.ts` — `Note`의 필드 3개를 확인합니다.
7. `src/user-profile.ts` — 작성자 이름을 얻는 방식을 봅니다.

## 다루지 않은 범위

`tsconfig.json`과 빌드 산출물 `dist/`는 읽지 않았습니다. 소스 5개, `package.json`, `README.md`는 모두 읽었습니다.
