---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62, package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, README.md: ad3e9d59c7f90caab58f57655039b71b09108d4876e83a62570fdae41ee77e70, docs/codemap/architecture.md: 8eca049d68973a1b7ac39eea77daca509e6ad1a05905d4f623f10b2b8e704d62, docs/codemap/dependency-graph.md: 3bb71e17ad5fe3cee22674e271c37e0ca2bd64bd076b498936e5f90b7b310941, docs/codemap/mindmap.md: 5243108c84621bb6d8f58083c9c3a5fdd5a9700e2457183b3afe168527c5a036, docs/codemap/sequence-flow.md: d8efe8e09a4a7166ee56cfb7408f4758aadd1b0126d5e609fa2c84205477e3b3}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Design doc and onboarding guide

How `notes-cli` is built, and in what order to read it.

## Overview

`notes-cli` is a command-line notes tool (`README.md`): `notes add "text"` stores a note and `notes list` prints the stored notes. It is written in TypeScript (strict mode, compiled with `tsc` to CommonJS per `package.json` and `tsconfig.json`) and runs on Node.js through the `notes` bin entry. It has no runtime dependencies; `typescript` is the only dev dependency.

## How it is structured

The code is five small files in `src/`: one entry file that dispatches commands, a notes store, a formatter, a user-name helper and a shared type. Diagrams are in `architecture.md` (system, containers, components), `dependency-graph.md` (imports; no cycles), `mindmap.md` (responsibilities) and `sequence-flow.md` (the `add`, `list` and error paths). The import direction is simple: `src/index.ts` → `src/notes-store.ts` → `src/format.ts` → `src/types.ts`, with `src/index.ts` also using `src/user-profile.ts`.

## Key design choices

1. **CLI parsing in a single entry file.** `src/index.ts` reads `process.argv`, branches on `add` / `list` and prints usage with exit code 1 otherwise. Effect: no argument-parsing library and one place to look for commands.
2. **In-memory storage behind a small module.** `src/notes-store.ts` keeps a module-level `notes` array and exposes only `addNote` and `listNotes`. Effect: callers are isolated from storage, but notes vanish when the process ends, so `notes list` in a new run is empty. Reason: not stated anywhere; probably a first version meant to be extended. (inferred) <!-- codemap:unverified -->
3. **Formatting separated from storage.** `src/format.ts` turns a `Note` into `#id text (author)` and the store maps over it. Effect: display format can change without touching storage.
4. **Author comes from the environment.** `src/user-profile.ts` returns `process.env.USER` or `"anonymous"`, and `src/index.ts` passes it to `addNote`. Effect: each note records who added it with no login or config.
5. **One shared type.** `src/types.ts` defines `Note` (`id`, `text`, `author`), imported by the store and the formatter. Effect: the data shape is defined once.

## Reading order (onboarding guide)

1. `README.md` — the two commands the tool supports.
2. `package.json` — the `notes` bin entry (build output `dist/index.js`) and the `build` script.
3. `src/index.ts` — where execution starts; see how commands map to calls.
4. `src/notes-store.ts` — the core logic; note the in-memory array and id scheme (length + 1).
5. `src/types.ts` — the `Note` shape used everywhere.
6. `src/format.ts` — how a note becomes a printed line.
7. `src/user-profile.ts` — the `USER` fallback logic, the only environment access.

## Not covered

All source files, `package.json` and `README.md` were read completely. `tsconfig.json` was only checked for the output folder. There are no tests in the repository, and the build output (`dist/`) does not exist, so neither was examined. Design reasons marked unverified are guesses, not facts from the repository.
