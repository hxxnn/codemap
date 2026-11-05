---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 의존성 그래프

`src` 안의 파일 5개가 실제 `import` 문으로 서로 연결된 모습이며, 화살표는 가져오는 쪽에서 가져오는 대상으로 향합니다.

```mermaid
flowchart LR
  n1["src/index.ts"]
  n2["src/notes-store.ts"]
  n3["src/user-profile.ts"]
  n4["src/format.ts"]
  n5["src/types.ts"]
  n1 --> n2
  n1 --> n3
  n2 --> n4
  n2 --> n5
  n4 --> n5
```

`src/index.ts`가 맨 위에서 두 모듈을 가져오고, 모든 길이 `src/types.ts`로 모입니다.

## 순환 의존

읽은 `import` 문 5개 파일 안에서 순환 의존과 자기 자신을 가져오는 경우는 발견되지 않았습니다.

## 가장 많이 가져다 쓰는 파일

- `src/types.ts` — 2곳(`src/notes-store.ts`, `src/format.ts`)에서 `Note`를 가져옵니다.
- `src/notes-store.ts` — `src/index.ts`가 `addNote`, `listNotes`를 가져옵니다.
- `src/user-profile.ts` — `src/index.ts`가 `currentUser`를 가져옵니다.
- `src/format.ts` — `src/notes-store.ts`가 `formatNote`를 가져옵니다.

## 다루지 않은 범위

외부 패키지 import는 없었고, 동적 import도 발견되지 않았습니다. `tsconfig.json`과 빌드 산출물 `dist/`는 읽지 않았으며, 나머지 소스 5개는 모두 읽었습니다.
