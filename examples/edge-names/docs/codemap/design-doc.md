---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d, package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, README.md: 20617bb945b32699044b85affe89774ed9278ec9a9586b92f1528162c250eddc, docs/codemap/architecture.md: 1d913ac79b8c246c8953950089a111b8fcbcb9f308b1ed2d9d90e2b1bf5f0d6b, docs/codemap/dependency-graph.md: 092f5354fdffc5909503b5d5039a406d2c49f0207db94c256994e2e832dd84a0, docs/codemap/mindmap.md: 310e0b8f312fe690a6034bb023c5d95d9ccf06a3c97a945d8bb338715640f52a, docs/codemap/sequence-flow.md: ab6917491e31ef924747c353d75e8e53342eaaa28b7bea99f4994a9faac820d4}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Design doc and onboarding guide

How `edge-names` is built and in what order to read it.

## Overview

`edge-names` is a small CommonJS Node.js script. According to `README.md`, it is a tiny project whose file names contain spaces and non-ASCII characters. When run, it takes a built-in list of three strings, upper-cases each, adds `!`, and prints them. It has no dependencies and no framework.

## How it is structured

The project is one container with three modules under `src/`: an entry file, a data source and a formatter. See `architecture.md` for the three zoom levels, `dependency-graph.md` for the imports (only `src/main.js` imports anything, with no cycles), `mindmap.md` for the overview and `sequence-flow.md` for the call order.

## Key design choices

1. **One entry file wires everything.** `src/main.js` is the only file that imports the others, so the data and formatting modules stay independent of each other. Effect: no cycles and a one-way flow of dependencies.
2. **Hard-coded data behind a function.** `src/데이터 로더.js` keeps the items in a module-level array and exposes `loadItems()`, which returns a copy via `slice()`. Effect: callers cannot mutate the stored list. Reason for the copy: inferred. <!-- codemap:unverified -->
3. **One small named export per module.** Both helper modules export a single function through `module.exports = { ... }`, and `src/main.js` destructures it. Effect: each import states exactly what is used.
4. **Entry point declared in the manifest.** `package.json` sets `main` to `src/main.js`.
5. **File names with spaces and non-ASCII characters.** `src/my utils.js` and `src/데이터 로더.js` are required by exact name with the `.js` extension. Effect: the names must be quoted in shell commands. The README describes this as the purpose of the project.

## Reading order (onboarding guide)

1. `README.md` — the one-line purpose and why the file names look unusual.
2. `package.json` — find `main`, which names the entry point.
3. `src/main.js` — the whole flow in six lines: two requires and a loop.
4. `src/데이터 로더.js` — where the items come from; note the `slice()` copy.
5. `src/my utils.js` — the formatting rule (`toUpperCase()` plus `"!"`).

## Not covered

Nothing was skipped: every source file, `package.json` and `README.md` were read in full. The script was not executed, and there are no tests in the project.
