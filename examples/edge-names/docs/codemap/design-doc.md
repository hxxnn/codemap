---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, README.md: 20617bb945b32699044b85affe89774ed9278ec9a9586b92f1528162c250eddc, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, docs/codemap/architecture.md: fcdf0d5976d4e372ee8b1aa7bf6e3369bc4eb21e3803e7c08280c899d7e14370, docs/codemap/dependency-graph.md: dcd46b9de0b673124c932738f163de181737cefcd7c386f38ae77172959962d8, docs/codemap/mindmap.md: 611900b9dd9fca7be4b579a39e75144c109ab12cb9be9c35e7e5100f987e2b1f, docs/codemap/sequence-flow.md: 26cb8ee5c8130c9fca9dd0ee54515845a80ab025ebb629dbf3452e6e36ca5c6d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 설계 문서와 온보딩 가이드

## 개요

`edge-names`는 `README.md`에 따르면 "파일 이름에 공백과 ASCII가 아닌 문자가 들어 있는 아주 작은 프로젝트"입니다. 실행하면 고정된 항목 세 개(`alpha`, `beta`, `gamma`)를 대문자로 바꾸고 느낌표를 붙여 콘솔에 한 줄씩 출력합니다. 기술은 외부 의존성이 없는 Node.js(CommonJS, `require`/`module.exports`)뿐입니다.

## 구조

코드는 `src/` 아래 파일 3개로 이루어집니다. `src/main.js`가 진입점이고, `src/my utils.js`(문자열 변환)와 `src/데이터 로더.js`(항목 제공)를 불러옵니다. 두 모듈은 서로를 알지 못하며, 화살표는 모두 진입점에서 바깥으로만 향합니다. 자세한 그림은 `architecture.md`, 의존 관계는 `dependency-graph.md`, 파일·함수 목록은 `mindmap.md`, 호출 순서는 `sequence-flow.md`를 보세요.

## 핵심 설계 선택

1. **진입 파일에서 흐름을 조립** — `src/main.js`가 두 모듈을 불러와 반복문 안에서 연결합니다. 모듈끼리의 결합이 없어 각각 따로 이해할 수 있습니다.
2. **모듈마다 함수 하나를 `module.exports`로 내보냄** — `src/my utils.js`는 `shout`, `src/데이터 로더.js`는 `loadItems`만 공개합니다. 공개 표면이 작습니다.
3. **데이터를 모듈 안 배열에 두고 복사본을 반환** — `src/데이터 로더.js`의 `loadItems()`는 `items.slice()`를 돌려줍니다. 호출자가 결과를 바꿔도 원본 배열은 영향을 받지 않는 효과가 있습니다. 이렇게 한 이유는 코드에 적혀 있지 않습니다 (추정) <!-- codemap:unverified -->.
4. **파일 이름에 공백과 한글을 의도적으로 사용** — `src/my utils.js`, `src/데이터 로더.js`가 그 예이며, `README.md`가 이 점을 프로젝트의 목적으로 밝힙니다. `require("./my utils.js")`처럼 경로를 문자열 그대로 적어야 하는 효과가 있습니다.
5. **외부 패키지 없음** — `package.json`에 의존성 항목이 없고 `main`만 `src/main.js`로 지정되어 있습니다.

## 읽는 순서 (온보딩 가이드)

1. `README.md` — 프로젝트의 목적(특이한 파일 이름)을 먼저 확인합니다.
2. `package.json` — `main`이 `src/main.js`를 가리키는지, 의존성이 없는지 봅니다.
3. `src/main.js` — 전체 흐름이 여기 있습니다. 두 `require`와 `for...of` 반복을 따라가세요.
4. `src/my utils.js` — `shout`가 문자열을 어떻게 바꾸는지 봅니다.
5. `src/데이터 로더.js` — 항목 배열과 `slice()`로 복사해 돌려주는 부분을 봅니다.

## 다루지 않은 범위

소스와 설정 파일을 모두 읽었고 건너뛴 폴더는 없습니다. 위 구조 설명은 코드를 직접 읽어 확인했습니다. 다만 `src/데이터 로더.js`는 경로에 한글이 있어 해시 안전 규칙을 통과하지 못해 `sources`에 넣지 못했습니다 (확인 필요) <!-- codemap:unverified -->.
