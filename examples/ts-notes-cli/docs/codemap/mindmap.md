---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 구조 트리

`notes-cli`를 기능별로 묶고 파일과 주요 함수까지 펼친 트리입니다.

- **notes-cli** — 메모를 추가하고 목록으로 보여 주는 작은 명령줄 도구
  - **CLI** — 명령어를 해석하는 층
    - `src/index.ts` — `add`, `list` 명령 분기와 사용법 출력
  - **저장소** — 메모를 메모리에 보관
    - `src/notes-store.ts` — 모듈 전역 배열에 메모 보관
      - `addNote()` — 번호를 붙여 메모를 추가
      - `listNotes()` — 메모를 문자열 목록으로 변환
  - **보조** — 작성자와 출력 형식
    - `src/user-profile.ts` — 현재 사용자 이름 제공
      - `currentUser()` — 환경변수 `USER`, 없으면 `anonymous`
    - `src/format.ts` — 메모 한 줄 문자열 만들기
      - `formatNote()` — `#번호 내용 (작성자)` 형태로 변환
  - **타입** — 공유 데이터 모양
    - `src/types.ts` — `Note` 인터페이스

## 그룹별 설명

- **CLI** — 사용자 입력의 유일한 진입점입니다.
- **저장소** — 영속 저장 없이 프로세스 메모리에만 둡니다.
- **보조** — 작성자 이름과 출력 모양을 각각 한 파일로 분리했습니다.
- **타입** — `Note` 하나뿐입니다. `package.json`, `README.md`, `tsconfig.json`은 트리에서 뺐습니다.

## 다루지 않은 범위

`tsconfig.json`과 빌드 산출물 `dist/`는 읽지 않았고, 소스 5개는 모두 읽었습니다.
