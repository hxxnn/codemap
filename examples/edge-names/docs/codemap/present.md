---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 6be7a76b01b05fdfed2e24d082c375e06c288eccb5856363b5734c23ee428531, docs/codemap/dependency-graph.md: 78772b1968602fe63142de9af69c2838f086d83c6025b683d5c34668a1f1e6bf, docs/codemap/sequence-flow.md: ac7bf7cf4f4a171a10f53cd656ddf80d59c7fdae1a6ad1c4a9396e2c709fd227, docs/codemap/design-doc.md: 05065e0b12ab9257e067d676993264d1ed7dc6823b67282c79183ba9a6a38dc2}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Presentation outline: edge-names

## Slide 1 — What it is
- A tiny Node.js script that prints `ALPHA!`, `BETA!`, `GAMMA!`.
- Entry point: `src/main.js`, declared in `package.json`.

## Slide 2 — Architecture
- One process, three files, no external systems (see `architecture.md`).

## Slide 3 — Dependencies
- `src/main.js` requires `src/my utils.js` and `src/데이터 로더.js`; no cycles, no npm packages (see `dependency-graph.md`).

## Slide 4 — Runtime flow
- Load items, then shout and print each one (see `sequence-flow.md`).

## Slide 5 — Design notes
- Defensive copy in `loadItems`; file names with a space and Hangul are used on purpose (see `design-doc.md`).

## Slide 6 — Where to start reading
- `package.json`, then `src/main.js`, then the two helpers.

## Not covered
Built only from the existing codemap files; no new code analysis.
