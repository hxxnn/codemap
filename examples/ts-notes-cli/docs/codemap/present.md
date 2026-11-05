---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 9db7a85e6b362e4c5c18f21b06766696ddfeaa2cb2c586d79939545e509ebb8b, docs/codemap/dependency-graph.md: 91c9072196ae3897e9b2d95dfcc3f4cd6557a3418825ae49f35fd92eef2a0661, docs/codemap/mindmap.md: 1b56d3af32ea633c2b1a4f8f81560b5eee55f12762252ae74c95d75a24f6dfc1, docs/codemap/sequence-flow.md: 74e892ecc97a58b3f979b50fa659c0225b330fbc540a90f1b1a6c6fcc43dad12, docs/codemap/design-doc.md: f1e76827d7e21038d28a4cc92e220f227e21033dd80da8d85a87c25fe3d1e2a0}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 발표 개요

`notes-cli`를 다른 사람에게 소개하기 위한 7장짜리 슬라이드 개요이며, 모든 내용은 기존 codemap 문서 5개(`architecture.md`, `dependency-graph.md`, `mindmap.md`, `sequence-flow.md`, `design-doc.md`)에서 가져왔습니다.

## 슬라이드 1: 무엇인가

`notes-cli`는 터미널에서 메모를 추가하고 목록을 보는 작은 명령줄 도구입니다. TypeScript로 작성되었고 런타임 의존성이 없으며, 메모는 프로세스 메모리에만 저장됩니다.

Show: `design-doc.md` → "개요" 섹션(텍스트만, 다이어그램 없음)

## 슬라이드 2: 큰 그림

사용자가 터미널에서 명령을 실행하면 하나의 Node.js 프로세스가 처리합니다. 프로세스 안에는 진입점과 메모리 저장소가 있고, 작성자 이름은 환경 변수 `USER`에서 얻습니다.

Show: `architecture.md` → "2단계: 컨테이너" 다이어그램

## 슬라이드 3: 어떻게 구성되어 있나

코드는 진입점, 저장소, 표시, 사용자 정보, 타입, 빌드 설정의 여섯 가지로 나뉩니다. 각 가지가 하나의 책임과 하나의 파일(또는 설정 파일)에 대응합니다.

Show: `mindmap.md` → "마인드맵" 다이어그램

## 슬라이드 4: 어떻게 실행되나

`notes add`를 실행하면 `src/index.ts`가 작성자를 조회하고 저장소에 메모를 추가합니다. 저장은 메모리 배열에만 일어나며 결과는 출력하지 않습니다.

Show: `sequence-flow.md` → "메모 추가: notes add" 다이어그램

## 슬라이드 5: 파일들은 서로 어떻게 의존하나

의존은 `src/index.ts`에서 `src/types.ts` 방향으로만 흐르고 순환 의존은 없습니다. 가장 많이 의존되는 파일은 `src/types.ts`입니다.

Show: `dependency-graph.md` → "의존성 그래프" 다이어그램

## 슬라이드 6: 핵심 설계 선택

메모리 배열 저장은 작은 모듈(`src/notes-store.ts`) 뒤에 숨겨져 있고, 명령 파싱은 `src/index.ts` 한 파일에서 라이브러리 없이 처리합니다. 두 선택의 이유는 코드에 적혀 있지 않습니다. (추정) <!-- codemap:unverified -->

환경 변수 접근은 `src/user-profile.ts`의 `currentUser` 한 곳에 모여 있습니다.

Show: `design-doc.md` → "핵심 설계 선택" 섹션(텍스트만, 다이어그램 없음)

## 슬라이드 7: 어디서부터 읽을까

`README.md`, `package.json`, `src/index.ts` 순서로 시작해 `src/notes-store.ts`와 `src/types.ts`로 내려가면 전체 흐름이 잡힙니다.

Show: `design-doc.md` → "읽는 순서" 섹션(텍스트만, 다이어그램 없음)

## 다루지 않은 범위

원본 문서들의 범위와 같습니다. 소스 파일 5개와 `README.md`, `package.json`, `tsconfig.json`을 모두 읽었고, 테스트와 CI 설정, 커밋 이력은 저장소에 없습니다. 빌드 산출물 dist/와 node_modules/도 저장소에 없습니다.
