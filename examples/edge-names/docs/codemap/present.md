---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: b66f362e7f2acb92ff52d43ec6b132250b6a83ec450b98d0a5fd07e403cb8d18, docs/codemap/dependency-graph.md: 9e276e4f40ace831ae920c3ce602b1de0603d5d09dd21e5dd813bf0a4e77b0e5, docs/codemap/mindmap.md: e42d2d8fb11875bd3269dd0bb6a4d10681c45e60d6ae5652a07440f6ab9ae24b, docs/codemap/sequence-flow.md: 2b848623d60393fd918cada3eadea07522f9e35499db41f26012fd374c5853e7, docs/codemap/design-doc.md: 0774dc3a0cb09b295a71a3318300c2194a7e4172296750d883cb55cd7f56db99}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 발표 개요

`edge-names` 코드베이스를 팀에 소개하기 위한 7장짜리 슬라이드 개요이며, 기존 codemap 문서 5개에서만 내용을 가져왔습니다.

## 슬라이드 1: 이게 무엇인가

고정된 항목 목록을 대문자로 바꿔 출력하는 아주 작은 Node.js 프로그램으로, 파일 이름에 공백과 한글이 들어간 경우를 시험하려는 프로젝트입니다. 외부 패키지는 쓰지 않습니다.
Show: `design-doc.md` → "개요"

## 슬라이드 2: 큰 그림

프로세스 하나가 사용자의 실행을 받아 결과를 터미널로 내보냅니다. 서버나 데이터베이스는 없습니다.
Show: `architecture.md` → "2단계: 컨테이너" 다이어그램

## 슬라이드 3: 어떻게 구성되어 있나

실행, 데이터, 문자열 변환 세 갈래로 나뉩니다.
Show: `mindmap.md` → 마인드맵 다이어그램

## 슬라이드 4: 어떻게 실행되나

`src/main.js`가 항목을 불러온 뒤 하나씩 변환하고 출력합니다.
Show: `sequence-flow.md` → "프로그램 실행: 항목을 대문자로 출력" 다이어그램

## 슬라이드 5: 파일끼리의 의존 관계

`src/main.js`만 다른 두 파일을 가져오며, 순환 의존은 없습니다.
Show: `dependency-graph.md` → 의존성 그래프 다이어그램

## 슬라이드 6: 핵심 설계 선택

역할별로 파일 하나씩 분리하고, 진입 파일은 조립만 맡습니다. 데이터는 모듈 안의 메모리 배열에 두고 복사본을 돌려줍니다. <!-- codemap:unverified --> (추정) 복사본을 돌려주는 이유는 코드에 적혀 있지 않습니다.
Show: `design-doc.md` → "핵심 설계 선택"

## 슬라이드 7: 어디서부터 읽을까

`README.md`, `package.json`, `src/main.js` 순서로 읽고, 그다음 `src/데이터 로더.js`와 `src/my utils.js`를 봅니다.
Show: `design-doc.md` → "읽는 순서 (온보딩 가이드)"

## 다루지 않은 범위

원본 문서들의 범위와 같습니다. 소스 파일 3개와 `package.json`, `README.md`를 모두 읽었으며, 읽지 않은 범위는 없습니다.
