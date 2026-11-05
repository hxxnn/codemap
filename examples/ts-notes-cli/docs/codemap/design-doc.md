---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62, package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, tsconfig.json: fbfb5e54f48dbca20aff45f6530b732e22d3c4fd596d106e199b9ee5ff9eb439, README.md: ad3e9d59c7f90caab58f57655039b71b09108d4876e83a62570fdae41ee77e70, docs/codemap/architecture.md: fabaf87a3aeb5141ee19be6283a4d4727a929ace6542da1e3da20eef52725ba0, docs/codemap/dependency-graph.md: 37de8c4b7a2765fed72da30bf7924d1c45e1ad42c27d048fc28b6812c6aacb0a, docs/codemap/mindmap.md: 5221fa8be8571bb10a223cc0fa7588328f199d0056142c1e646c672f4496743f, docs/codemap/sequence-flow.md: 94ed8888679da195a714b8251db773b141fd62b43e2cf91b62542ad81230d071}
---

<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->


# Design doc and onboarding guide

How `notes-cli` is built and in what order to read it.

## Overview

`notes-cli` is a command-line notes tool (`README.md`): `notes add "text"` stores a note and `notes list` prints all notes. It is written in TypeScript (`typescript` ^5.4.0 in `package.json`), compiled with `tsc` to dist/ (build output) in CommonJS format (`tsconfig.json`), and exposed as the `notes` binary. It has no runtime dependencies.

## How it is structured

The tool is one Node.js process with five small modules in `src/`: an entry file, a notes store, a user lookup, a formatter and a shared type. The entry file calls the store and user lookup; the store calls the formatter; the type is shared. See `architecture.md` for the three zoom levels, `dependency-graph.md` for the import edges (acyclic), `mindmap.md` for the overview and `sequence-flow.md` for the `add`, `list` and error flows.

## Key design choices

1. **CLI parsing in a single entry file.** `src/index.ts` reads `process.argv` and uses an `if / else if / else` on the command name. Effect: easy to read, but each new command adds another branch there. No reason is stated in the repo. The rationale is inferred. <!-- codemap:unverified -->
2. **In-memory storage behind a small module.** `src/notes-store.ts` keeps a module-level `notes` array and exposes only `addNote` and `listNotes`. Effect: notes are lost when the process exits, so `notes list` in a new run is always empty. Swapping in file storage would only touch this module. That last point is inferred. <!-- codemap:unverified -->
3. **Author taken from the environment.** `src/user-profile.ts` returns `process.env.USER ?? "anonymous"`. Effect: no login or config is needed; the name falls back to "anonymous" when `USER` is unset.
4. **Formatting separated from storage.** `src/format.ts` holds `formatNote`, which `src/notes-store.ts` maps over its array. Effect: output format changes in one place. The motivation is inferred. <!-- codemap:unverified -->
5. **Shared type in its own file.** `src/types.ts` defines the `Note` interface (`id`, `text`, `author`) used by `src/notes-store.ts` and `src/format.ts`. Effect: no import cycles (see `dependency-graph.md`).
6. **Strict TypeScript.** `tsconfig.json` sets `"strict": true`. Effect: stricter compile-time checks across `src/`.

## Reading order (onboarding guide)

1. `README.md`: the two supported commands.
2. `package.json`: the `notes` bin pointing at dist/index.js and the `build` script.
3. `src/index.ts`: the entry point; see how `add` and `list` are dispatched and where the usage error is.
4. `src/notes-store.ts`: the core logic; note the in-memory array and how ids are assigned (`notes.length + 1`).
5. `src/types.ts`: the `Note` shape used everywhere.
6. `src/format.ts`: how a note becomes the printed line `#id text (author)`.
7. `src/user-profile.ts`: where the author name comes from.
8. `tsconfig.json`: compiler settings (target ES2022, CommonJS, strict, output to dist/).

## Not covered

Nothing was skipped: every file in the repository (all of `src/`, `package.json`, `tsconfig.json`, `README.md`) was read. There are no tests and no dist/ folder in the repo.
