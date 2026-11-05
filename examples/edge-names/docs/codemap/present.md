---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: a1dce4c80ed5d37e8b4c9414f13db76f5b269fd2b1f1e5115434d20dcfa72007, docs/codemap/dependency-graph.md: c8fb1e5cd1f6f020e04505984a32d70b563429d7e34d044d876bbb45d4517eea, docs/codemap/mindmap.md: 92aea1c5aba96bbd0c68db5b1829e178e299ed47d97e8f5eb3ef0b84942c8bae, docs/codemap/sequence-flow.md: e09ddff9e734bca61596933de13e2710026e3a91df179d728ab20f0409c9d4ec, docs/codemap/design-doc.md: 580cc28453e869f0bb4199d450a4bd154c16dc8aa0686d2022b43843cdb81b4b}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Presentation outline

A seven-slide walkthrough of `edge-names`, built from the existing codemap artifacts; all five source artifacts were available.

## Slide 1: What it is
A tiny Node.js (CommonJS) program that prints `alpha`, `beta`, `gamma` in upper case with a `!`. Its file names contain spaces and non-ASCII characters (per `README.md`).
Show: `design-doc.md` → "Overview"

## Slide 2: The big picture
One CLI script run by a terminal user, writing to standard output. No database or network.
Show: `architecture.md` → "Level 2: Containers" diagram

## Slide 3: How it is organized
Three groups, one file each: entry point, data, formatting.
Show: `mindmap.md` → "Mindmap" diagram

## Slide 4: How it runs
`src/main.js` loads the items, shouts each one, and logs it.
Show: `sequence-flow.md` → "Run `node src/main.js`" diagram

## Slide 5: How the parts depend on each other
`src/main.js` requires both helpers; the helpers import nothing; there are no circular dependencies.
Show: `dependency-graph.md` → "Dependency graph" diagram

## Slide 6: Key design choices
The data module returns a copy of its array, and formatting lives in a pure helper. The reason for wiring everything in the entry script is not stated in the code. <!-- codemap:unverified --> (inferred)
Show: `design-doc.md` → "Key design choices"

## Slide 7: Where to start reading
Read `README.md`, `package.json`, `src/main.js`, then `src/데이터 로더.js` and `src/my utils.js`.
Show: `design-doc.md` → "Reading order (onboarding guide)"

## Not covered

All artifacts report that the repository was read completely; nothing was skipped.
