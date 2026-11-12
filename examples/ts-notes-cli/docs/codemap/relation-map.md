---
codemap: 1
skill: relation-map
generated_at: 2026-11-12
commit: null
sources: {src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 파일 관계 지도

`notes-cli`의 소스 파일 5개가 서로 어떤 파일을 가져다 쓰는지(import)를 실제 코드에서 읽어 정리했습니다. 화살표는 "가져오는 파일 → 가져온 파일" 방향입니다.

## 파일 표

| 파일 | 역할 | 쓰는 파일 | 쓰이는 파일 |
|---|---|---|---|
| `src/format.ts` | 메모 한 건을 한 줄 문자열로 만듦 | `src/types.ts` | `src/notes-store.ts` |
| `src/index.ts` | CLI 진입점, add·list 명령을 나눠 실행함 | `src/notes-store.ts`, `src/user-profile.ts` | — |
| `src/notes-store.ts` | 메모를 메모리에 쌓고 목록 문자열을 만듦 | `src/format.ts`, `src/types.ts` | `src/index.ts` |
| `src/types.ts` | 메모(Note) 데이터 모양을 정의함 | — | `src/format.ts`, `src/notes-store.ts` |
| `src/user-profile.ts` | 환경변수 USER로 현재 사용자 이름을 알려줌 | — | `src/index.ts` |

## 많이 쓰이는 파일

- `src/types.ts` — 2곳에서 사용 (`src/format.ts`, `src/notes-store.ts`)
- `src/format.ts` — 1곳에서 사용 (`src/notes-store.ts`)
- `src/notes-store.ts` — 1곳에서 사용 (`src/index.ts`)
- `src/user-profile.ts` — 1곳에서 사용 (`src/index.ts`)

## 순환 의존

순환 의존은 발견되지 않았습니다. 의존 방향은 `src/index.ts` → `src/notes-store.ts` → `src/format.ts` → `src/types.ts` 한 방향으로만 흐릅니다.

## 다루지 않은 범위

- 소스 파일 5개(`src/` 전체)를 모두 끝까지 읽었고, 동적 import·리플렉션·런타임 플러그인 로딩은 발견되지 않았습니다.
- 테스트 파일은 없습니다.
- 소스가 아닌 `README.md`, `tsconfig.json`, `package.json`은 import 관계의 근거가 아니므로 열어 분석하지 않았습니다(빌드 결과물 `dist/`는 저장소에 없음).
