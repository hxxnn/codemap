---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: fcdf0d5976d4e372ee8b1aa7bf6e3369bc4eb21e3803e7c08280c899d7e14370, docs/codemap/dependency-graph.md: dcd46b9de0b673124c932738f163de181737cefcd7c386f38ae77172959962d8, docs/codemap/mindmap.md: 611900b9dd9fca7be4b579a39e75144c109ab12cb9be9c35e7e5100f987e2b1f, docs/codemap/sequence-flow.md: 26cb8ee5c8130c9fca9dd0ee54515845a80ab025ebb629dbf3452e6e36ca5c6d, docs/codemap/design-doc.md: 1c26021525bbd6abbd21419cdff3b1e9f861aaed6e31fa995fb4464bf1a64ecd}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 발표 개요

`edge-names` 코드베이스를 다른 사람에게 설명하기 위한 7장짜리 슬라이드 구성입니다. 다섯 가지 codemap 문서가 모두 있어 빠진 출처는 없습니다.

## 슬라이드 1: 이게 무엇인가

공백과 한글이 들어간 파일 이름을 다루는 아주 작은 Node.js 프로젝트로, 항목 세 개를 대문자로 바꿔 콘솔에 출력합니다. 외부 의존성은 없습니다.

Show: `design-doc.md` → "개요"

## 슬라이드 2: 큰 그림

실행하는 사람이 `src/main.js`를 돌리면 결과가 콘솔로만 나갑니다. 배포 단위는 `src/`의 스크립트 하나입니다.

Show: `architecture.md` → "2단계: 컨테이너" 다이어그램

## 슬라이드 3: 어떻게 구성되어 있나

진입점, 문자열 가공, 데이터 세 묶음으로 나뉘고 파일은 모두 3개입니다.

Show: `mindmap.md` → 구조 트리

## 슬라이드 4: 어떻게 실행되나

진입점이 모듈 두 개를 불러온 뒤, 받은 항목마다 `shout()`로 바꿔 출력합니다.

Show: `sequence-flow.md` → "프로그램을 실행해 모든 항목을 출력하기" 다이어그램

## 슬라이드 5: 부분들이 서로 어떻게 의존하나

`src/main.js`가 나머지 두 파일을 불러오고, 두 파일은 서로를 모릅니다. 순환 의존은 발견되지 않았습니다.

Show: `dependency-graph.md` → "의존성 그래프" 다이어그램

## 슬라이드 6: 핵심 설계 선택

진입 파일이 흐름을 조립하고, 모듈은 함수 하나씩만 내보냅니다. `loadItems()`는 원본 대신 `items.slice()` 복사본을 돌려주는데, 그 이유는 코드에 적혀 있지 않습니다 (추정) <!-- codemap:unverified -->.

Show: `design-doc.md` → "핵심 설계 선택"

## 슬라이드 7: 어디서부터 읽을까

`README.md`, `package.json`, `src/main.js` 순으로 읽으면 목적과 전체 흐름을 가장 빨리 잡을 수 있습니다.

Show: `design-doc.md` → "읽는 순서 (온보딩 가이드)"

## 다루지 않은 범위

각 문서의 범위를 따릅니다. 소스 3개와 설정 파일을 모두 읽었고 건너뛴 폴더는 없습니다. `src/데이터 로더.js`는 경로에 한글이 있어 해시 안전 규칙을 통과하지 못해 각 문서의 `sources`에서 빠져 있습니다 (확인 필요) <!-- codemap:unverified -->.
