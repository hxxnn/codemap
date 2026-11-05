---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {README.md: 20617bb945b32699044b85affe89774ed9278ec9a9586b92f1528162c250eddc, package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d, docs/codemap/architecture.md: b66f362e7f2acb92ff52d43ec6b132250b6a83ec450b98d0a5fd07e403cb8d18, docs/codemap/dependency-graph.md: 9e276e4f40ace831ae920c3ce602b1de0603d5d09dd21e5dd813bf0a4e77b0e5, docs/codemap/mindmap.md: e42d2d8fb11875bd3269dd0bb6a4d10681c45e60d6ae5652a07440f6ab9ae24b, docs/codemap/sequence-flow.md: 2b848623d60393fd918cada3eadea07522f9e35499db41f26012fd374c5853e7}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 설계 문서와 온보딩 가이드

## 개요

`edge-names`는 `README.md`에 따르면 파일 이름에 공백과 한글이 들어간 경우를 시험하기 위한 작은 프로젝트입니다. 실행하면 고정된 항목 목록(`alpha`, `beta`, `gamma`)을 불러와 각 항목을 대문자로 바꾸고 `!`를 붙여 한 줄씩 출력합니다. 기술은 Node.js(CommonJS `require`)뿐이고 외부 패키지는 없습니다.

## 구조

프로세스 하나가 `src/main.js`에서 시작해 `src/데이터 로더.js`와 `src/my utils.js`를 불러 쓰는 단순한 구조입니다. 단계별 다이어그램은 `architecture.md`, 파일 간 import는 `dependency-graph.md`, 전체 지도는 `mindmap.md`, 실행 순서는 `sequence-flow.md`에 있습니다. 순환 의존은 없습니다.

## 핵심 설계 선택

1. **역할별로 파일 하나씩 분리**: 데이터 제공은 `src/데이터 로더.js`, 문자열 변환은 `src/my utils.js`, 조립은 `src/main.js`가 맡습니다. 효과는 각 파일이 함수 하나만 내보내 읽기 쉽다는 점입니다.
2. **진입 파일이 조립만 담당**: `src/main.js`는 불러오기와 출력 반복만 하고 변환 로직은 갖지 않습니다.
3. **데이터를 모듈 안의 메모리 배열로 보관**: `src/데이터 로더.js`는 `items` 배열을 두고 `slice()` 복사본을 돌려주어 호출자가 원본을 바꾸지 못합니다. 복사본을 돌려주는 이유가 코드나 주석에 적혀 있지는 않습니다. <!-- codemap:unverified --> (추정) 원본 보호가 의도였을 가능성이 있습니다.
4. **CommonJS 모듈 형식**: 세 파일 모두 `require`와 `module.exports`를 씁니다 (`src/main.js`, `src/my utils.js`, `src/데이터 로더.js`).
5. **파일 이름에 공백과 한글 사용**: `src/my utils.js`, `src/데이터 로더.js`가 그 예이며, `README.md`가 이를 프로젝트의 목적으로 밝히고 있습니다.

## 읽는 순서 (온보딩 가이드)

1. `README.md`: 프로젝트가 무엇을 시험하려는지 확인합니다.
2. `package.json`: `main`이 `src/main.js`인지, 의존 패키지가 없는지 확인합니다.
3. `src/main.js`: 전체 흐름이 여기서 조립됩니다. `require` 두 줄과 반복문을 보세요.
4. `src/데이터 로더.js`: `loadItems()`가 무엇을 돌려주는지, 왜 `slice()`를 쓰는지 봅니다.
5. `src/my utils.js`: `shout()`의 변환 규칙을 확인합니다.

## 다루지 않은 범위

프로젝트의 모든 소스와 설정 파일(`README.md`, `package.json`, `src/` 아래 3개)을 읽었으며, 읽지 않은 범위는 없습니다. 테스트와 빌드 설정은 저장소에 존재하지 않았습니다.
