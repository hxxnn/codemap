---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, docs/codemap/architecture.md: 909b01b2407810e88605d208577d203e42830720d57f7aa6fc45b448054a9698, docs/codemap/dependency-graph.md: 291b479a9d4ef0778d78742c57460ba5a1371a5a6a08c8712c28e96a77963e6d, docs/codemap/mindmap.md: dccc14b94f6e60422fd699c49c590d6aae03b93a3f2fc360a99790c721057c63, docs/codemap/sequence-flow.md: 15f76e01be5ce8ae4ea6c736344f7eda793d69921637462d6492cab330aa7978}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Design doc

## Overview
`edge-names` (`package.json`, main `src/main.js`) is a tiny CommonJS program. `src/main.js` loads items from `src/데이터 로더.js` and prints each one through `shout()` from `src/my utils.js`.

## Key design choices
- Each module exports one function via `module.exports`.
- `loadItems()` returns `items.slice()`, so callers get a copy and cannot mutate the module's list.
- File names contain spaces and non-ASCII characters, and imports use the exact names. The README describes the project as a test of such names.
- Why the project was built this way is not stated in the code. <!-- codemap:unverified --> (unverified)

## Reading order
1. `package.json`
2. `src/main.js`
3. `src/my utils.js`
4. `src/데이터 로더.js`

See also `architecture.md`, `dependency-graph.md`, `mindmap.md`, `sequence-flow.md`.

## Not covered
The repo was read completely. `src/데이터 로더.js` was read but is not listed in `sources` because its non-ASCII file name fails the safe-hashing rule (needs your decision).
