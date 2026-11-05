---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {README.md: ad3e9d59c7f90caab58f57655039b71b09108d4876e83a62570fdae41ee77e70, package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, tsconfig.json: fbfb5e54f48dbca20aff45f6530b732e22d3c4fd596d106e199b9ee5ff9eb439, src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62, docs/codemap/architecture.md: 9db7a85e6b362e4c5c18f21b06766696ddfeaa2cb2c586d79939545e509ebb8b, docs/codemap/dependency-graph.md: 91c9072196ae3897e9b2d95dfcc3f4cd6557a3418825ae49f35fd92eef2a0661, docs/codemap/mindmap.md: 1b56d3af32ea633c2b1a4f8f81560b5eee55f12762252ae74c95d75a24f6dfc1, docs/codemap/sequence-flow.md: 74e892ecc97a58b3f979b50fa659c0225b330fbc540a90f1b1a6c6fcc43dad12}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 설계 문서와 온보딩 가이드

`notes-cli`가 어떻게 만들어졌는지 설명하고, 처음 읽는 사람을 위해 코드를 읽을 순서를 안내하는 문서입니다.

## 개요

`notes-cli`는 터미널에서 메모를 추가(`notes add "text"`)하고 목록을 보는(`notes list`) 명령줄 도구이며, `README.md`도 같은 사용법을 설명합니다. TypeScript 5.4 이상으로 작성되었고(`package.json`) 컴파일 대상은 ES2022, 모듈 방식은 CommonJS, `strict` 모드입니다(`tsconfig.json`). 런타임 의존성은 없고 개발 의존성은 `typescript`뿐입니다. 메모는 프로세스 메모리 배열에만 저장됩니다.

## 구조

프로젝트는 하나의 CLI 프로세스이고, `src/` 아래 5개 파일이 진입점, 저장소, 포맷터, 사용자 정보, 타입으로 나뉘어 있습니다. 의존 방향은 위에서 아래로만 흐르며 순환은 없습니다. 자세한 그림은 `architecture.md`(세 단계 구조), `dependency-graph.md`(import 간선), `mindmap.md`(기능 지도), `sequence-flow.md`(`add`, `list`, 오류 경로의 호출 순서)를 보세요.

요약하면 `src/index.ts`가 `src/notes-store.ts`와 `src/user-profile.ts`를 부르고, 저장소는 `src/format.ts`로 출력 문자열을 만들며, `src/types.ts`의 `Note`를 공유합니다.

## 핵심 설계 선택

1. **메모리 배열 저장을 작은 모듈 뒤에 숨김.** `src/notes-store.ts`가 모듈 수준 배열 `notes`를 가지고 `addNote`와 `listNotes`만 내보냅니다. 효과: 호출부는 저장 방식을 몰라도 되지만, 프로세스가 끝나면 메모가 사라지므로 `notes add` 다음에 별도로 실행한 `notes list`에는 아무것도 나오지 않습니다. 이렇게 한 이유는 코드와 `README.md`에 적혀 있지 않습니다. 단순함을 위한 초기 단계 선택으로 보이지만 근거는 없습니다. (추정) <!-- codemap:unverified -->
2. **명령줄 파싱을 진입점 한 파일에서 직접 처리.** `src/index.ts`가 `process.argv.slice(2)`를 구조분해하고 `if / else if / else`로 분기하며, 인자 처리 라이브러리를 쓰지 않습니다(`package.json`에 런타임 의존성 없음). 효과: 명령이 두 개뿐이라 한 화면에서 전체 흐름이 보입니다. 라이브러리를 쓰지 않은 이유는 코드에 나와 있지 않습니다. (추정) <!-- codemap:unverified -->
3. **공유 타입을 별도 파일로 분리.** `src/types.ts`가 `Note`(`id`, `text`, `author`)만 정의하고, `src/notes-store.ts`와 `src/format.ts`가 이를 가져다 씁니다. 효과: 저장소와 포맷터가 서로를 거치지 않고 같은 형태를 공유합니다.
4. **표시 형식을 순수 함수로 분리.** `src/format.ts`의 `formatNote`는 `Note`를 받아 `#id 본문 (작성자)` 문자열만 돌려줍니다. 효과: 출력 형식을 바꿀 때 저장 로직을 건드리지 않아도 됩니다. 저장소는 `notes.map(formatNote)`로 이를 사용합니다.
5. **환경 의존을 한 함수에 격리.** `src/user-profile.ts`의 `currentUser`가 `process.env.USER`를 읽고 없으면 `"anonymous"`를 반환합니다. 효과: 환경 변수 접근이 이 한 곳에만 있어 나머지 코드가 `process.env`를 직접 알 필요가 없습니다.
6. **저장소가 문자열 목록을 반환.** `listNotes`가 `Note`가 아니라 포맷된 `string[]`을 돌려주므로 저장소가 표시 형식에 의존합니다(`src/notes-store.ts`가 `src/format.ts`를 가져옴). 효과: 진입점은 단순해지지만 저장과 표시가 한 모듈에서 만납니다.

## 읽는 순서

1. `README.md`: 도구의 목적과 두 명령의 사용법부터 확인합니다.
2. `package.json`: `bin`의 `notes` 항목과 `build` 스크립트(`tsc`), 개발 의존성만 있다는 점을 봅니다.
3. `src/index.ts`: 전체 흐름이 시작되는 곳입니다. `add`, `list`, 오류 분기 세 갈래를 찾아보세요.
4. `src/notes-store.ts`: 메모가 실제로 쌓이는 곳입니다. 모듈 수준 배열과 id 부여 방식(`notes.length + 1`)을 보세요.
5. `src/types.ts`: 모든 모듈이 공유하는 `Note`의 세 필드를 확인합니다.
6. `src/format.ts`: 출력 한 줄의 형식이 여기서 정해집니다.
7. `src/user-profile.ts`: 작성자 이름이 어디서 오는지, 기본값이 무엇인지 봅니다.
8. `tsconfig.json`: 컴파일 옵션(`strict`, `outDir`)으로 마무리합니다.

## 다루지 않은 범위

소스 파일 5개와 `README.md`, `package.json`, `tsconfig.json`을 모두 읽었습니다. 테스트 코드와 CI 설정, 커밋 이력은 저장소에 없어 근거로 쓰지 못했습니다. 빌드 산출물 dist/와 node_modules/도 저장소에 없습니다. 다른 codemap 문서 4개는 모두 존재해 그 내용을 재사용했습니다.
