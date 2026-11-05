---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 0b3d1389317e9a0ab4fcb87446bf55dd34567826c9c1d89d3aa18a4811970932, docs/codemap/dependency-graph.md: aaa5364d6b569e97ed9c72dd055cca72632c28d218b04d52f7ab502ab70f0fd1, docs/codemap/mindmap.md: de0ef7d606a8d96be6c3780193bf9e99e1dcb2477c15b6e7a5935ef5e3981b3e, docs/codemap/sequence-flow.md: 015eee2d2ee144769340373a10396a28dcd96430248ba4df188439328af1efa9, docs/codemap/design-doc.md: d263b0998e0de2f4fd5f290874c8dac68c689f3a5a9eccd0ac585f3c8bc2cdb6}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 발표 개요

`notes-cli`를 팀에 소개하기 위한 7장짜리 슬라이드 개요이며, 다섯 개 codemap 문서가 모두 있어 빠진 출처는 없습니다.

## 슬라이드 1: 무엇인가

터미널에서 `notes add`, `notes list`로 메모를 다루는 작은 TypeScript 명령줄 도구입니다.
Show: `design-doc.md` → "개요"

## 슬라이드 2: 큰 그림

사용자 한 명, 프로세스 하나, 메모리 배열 하나로 이루어진 단순한 구조입니다.
Show: `architecture.md` → "2. 컨테이너" 다이어그램

## 슬라이드 3: 어떻게 구성되어 있나

CLI, 저장소, 보조, 타입 네 묶음으로 나뉘며 파일은 모두 `src/` 아래에 있습니다.
Show: `mindmap.md` → 구조 트리

## 슬라이드 4: 어떻게 실행되나

`notes list`는 저장소가 각 메모를 포맷터에 넘겨 한 줄씩 만든 뒤 진입 파일이 출력합니다.
Show: `sequence-flow.md` → "notes list 실행" 다이어그램

## 슬라이드 5: 부분들의 의존 관계

모든 의존이 `src/types.ts`로 모이고, 순환 의존은 없습니다.
Show: `dependency-graph.md` → 의존성 그래프 다이어그램

## 슬라이드 6: 핵심 설계 선택

메모는 모듈 전역 배열에만 있어 프로세스가 끝나면 사라지고, 그 이유는 코드에 적혀 있지 않습니다. (추정: 프로토타입이라서) <!-- codemap:unverified -->
또한 출력 형식을 `src/format.ts`로 분리해 저장 로직과 독립시켰습니다.
Show: `design-doc.md` → "핵심 설계 선택"

## 슬라이드 7: 어디부터 읽을까

`README.md`, `package.json`, `src/index.ts`, `src/notes-store.ts` 순서로 읽으면 흐름이 잡힙니다.
Show: `design-doc.md` → "읽는 순서"

## 다루지 않은 범위

`tsconfig.json`과 빌드 산출물 `dist/`는 읽지 않았고, 소스 5개는 모두 읽었습니다.
