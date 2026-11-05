---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 6be7a76b01b05fdfed2e24d082c375e06c288eccb5856363b5734c23ee428531, docs/codemap/dependency-graph.md: 78772b1968602fe63142de9af69c2838f086d83c6025b683d5c34668a1f1e6bf, docs/codemap/mindmap.md: c876a4940ba86e4170e0f0deef3056f7b7f8628b519115cf5c2da14ef37b0329, docs/codemap/sequence-flow.md: ac7bf7cf4f4a171a10f53cd656ddf80d59c7fdae1a6ad1c4a9396e2c709fd227, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Design doc: edge-names

## Overview
`edge-names` is a tiny Node.js (CommonJS) script. `package.json` sets `main` to `src/main.js`, which prints each loaded item in upper case followed by `!`. See `architecture.md` for the diagrams.

## Key design choices
- **Three small modules.** Loading data (`src/데이터 로더.js`), formatting (`src/my utils.js`) and orchestration (`src/main.js`) are separate files.
- **Defensive copy.** `loadItems` returns `items.slice()`, so callers cannot mutate the module's list.
- **Unusual file names.** Two files have a space or Hangul in their names, and `require` uses those names verbatim. The README says this is the project's purpose (an edge case for names).
- **Why it was built this way** (a test fixture for tools handling odd file names) is only suggested by the README. <!-- codemap:unverified --> (inferred)

## Reading order for newcomers
1. `package.json` — find the entry point.
2. `src/main.js` — the whole control flow in six lines.
3. `src/데이터 로더.js` — where the data comes from.
4. `src/my utils.js` — the formatting helper.

## Not covered
The whole repository was read; the script was not executed.
