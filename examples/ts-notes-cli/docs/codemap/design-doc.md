---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {README.md: ad3e9d59c7f90caab58f57655039b71b09108d4876e83a62570fdae41ee77e70, package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62, docs/codemap/architecture.md: 65244941c9216c0d9ec17a4f16412cbca94d47d5a984ce52e2f44c954f2fdb1f, docs/codemap/dependency-graph.md: 83dfb3cc76426cf175db0d926f6b78c6592aa785e1c7c26e1ed8c7af296d4b3a, docs/codemap/mindmap.md: 4cd2ca6623fdc5bdfc4b7f3b9ead3eca670be36df5a042fe32af127d9e85c637, docs/codemap/sequence-flow.md: a6c50be6a75847a39133c7678a8617d4a14b6265c2716c1adfd72891b9f3108c}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Design doc and onboarding guide

## Overview

`notes-cli` is a command-line notes tool, described in `README.md` as `notes add "text"` and `notes list`. It is written in TypeScript and compiled with `tsc` (`package.json`), and it runs on Node.js with `typescript` as its only dependency. Each note has an id, text and author, and the author is taken from the `USER` environment variable.

## How it is structured

The project is one process with five small source files under `src/`: an entry file, a store, a formatter, a user-profile helper and a type file. See `architecture.md` for the three zoom levels, `dependency-graph.md` for the imports (no cycles), `mindmap.md` for the grouping and `sequence-flow.md` for the `add`, `list` and error flows. In short, `src/index.ts` calls `src/notes-store.ts` and `src/user-profile.ts`, and the store calls `src/format.ts`.

## Key design choices

1. **Notes live in memory behind a small module.** `src/notes-store.ts` keeps a module-level `notes` array and exposes only `addNote` and `listNotes`. Effect: nothing is persisted, so each run of the program starts empty and `notes list` in a new process prints nothing. Reason: not stated in the code. (inferred) <!-- codemap:unverified -->
2. **Command parsing happens in the entry file.** `src/index.ts` reads `process.argv` directly and branches on `add` and `list`, with no CLI library. Effect: unknown commands print a usage line to standard error and exit with code 1. Reason: not stated in the code. (inferred) <!-- codemap:unverified -->
3. **Formatting is separate from storage.** `src/format.ts` holds `formatNote`, and the store maps notes through it in `listNotes`. Effect: display format can change without touching storage logic. Reason: not stated in the code. (inferred) <!-- codemap:unverified -->
4. **One shared `Note` interface.** `src/types.ts` defines it and both `src/notes-store.ts` and `src/format.ts` import it. Effect: the note shape has a single definition. Reason: not stated in the code. (inferred) <!-- codemap:unverified -->
5. **Author comes from the environment with a fallback.** `src/user-profile.ts` returns `process.env.USER ?? "anonymous"`. Effect: no login or configuration is needed, and the name is `anonymous` when `USER` is unset. Reason: not stated in the code. (inferred) <!-- codemap:unverified -->

## Reading order (onboarding guide)

1. `README.md` — the two commands the tool offers.
2. `package.json` — the `notes` binary points to build output `dist/index.js`, and `npm run build` runs `tsc`.
3. `src/index.ts` — the entry point; see how `add` and `list` are dispatched and what happens on bad input.
4. `src/notes-store.ts` — the core logic; note the module-level array and how ids are assigned (`notes.length + 1`).
5. `src/format.ts` — the one-line output format `#id text (author)`.
6. `src/types.ts` — the `Note` interface used by the store and formatter.
7. `src/user-profile.ts` — the smallest file; where the author name comes from.

## Not covered

The small repo was read completely except `tsconfig.json`, which was not opened. Nothing is vendored or generated, and no test files exist in the repo.
