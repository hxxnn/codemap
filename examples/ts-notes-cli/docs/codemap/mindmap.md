---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, tsconfig.json: fbfb5e54f48dbca20aff45f6530b732e22d3c4fd596d106e199b9ee5ff9eb439, src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 마인드맵

`notes-cli`를 기능별로 묶어 한눈에 보여 주는 마인드맵입니다.

```mermaid
mindmap
  root((notes-cli))
    n1["진입점 / CLI"]
      n2["src/index.ts: add, list 명령 분기"]
    n3["저장소"]
      n4["src/notes-store.ts: 메모리 배열에 저장"]
        n5["addNote()"]
        n6["listNotes()"]
    n7["표시"]
      n8["src/format.ts: 메모 한 줄 포맷"]
        n9["formatNote()"]
    n10["사용자 정보"]
      n11["src/user-profile.ts: USER 환경 변수"]
        n12["currentUser()"]
    n13["타입"]
      n14["src/types.ts: Note 인터페이스"]
    n15["빌드 설정"]
      n16["package.json: bin, tsc 빌드"]
      n17["tsconfig.json: strict, ES2022"]
```

각 가지는 한 가지 책임을 맡고, 그 아래에 실제로 읽은 파일과 대표 함수를 두었습니다.

## 그룹

- 진입점 / CLI: 명령줄 인자를 읽어 `add`, `list` 또는 사용법 오류로 분기합니다(`src/index.ts`).
- 저장소: 메모를 프로세스 메모리의 배열에 쌓고 조회합니다(`src/notes-store.ts`).
- 표시: `Note` 하나를 `#id 본문 (작성자)` 문자열로 바꿉니다(`src/format.ts`).
- 사용자 정보: 작성자 이름으로 쓸 현재 사용자를 돌려줍니다(`src/user-profile.ts`).
- 타입: 모듈 사이에서 공유하는 `Note` 형태를 정의합니다(`src/types.ts`).
- 빌드 설정: `notes` 실행 파일 선언과 TypeScript 컴파일 옵션입니다(`package.json`, `tsconfig.json`). 빼 둔 항목은 없습니다.

## 다루지 않은 범위

소스 파일 5개와 설정 파일 2개를 모두 읽었습니다. 빌드 산출물 dist/와 node_modules/는 저장소에 없습니다.
