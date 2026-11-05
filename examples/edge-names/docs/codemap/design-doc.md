---
codemap: 1
skill: design-doc
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d, package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, README.md: 20617bb945b32699044b85affe89774ed9278ec9a9586b92f1528162c250eddc, docs/codemap/architecture.md: a1dce4c80ed5d37e8b4c9414f13db76f5b269fd2b1f1e5115434d20dcfa72007, docs/codemap/dependency-graph.md: c8fb1e5cd1f6f020e04505984a32d70b563429d7e34d044d876bbb45d4517eea, docs/codemap/mindmap.md: 92aea1c5aba96bbd0c68db5b1829e178e299ed47d97e8f5eb3ef0b84942c8bae, docs/codemap/sequence-flow.md: e09ddff9e734bca61596933de13e2710026e3a91df179d728ab20f0409c9d4ec}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Design doc and onboarding guide

## Overview

`edge-names` is a tiny Node.js (CommonJS) command-line program. Running `src/main.js` prints each item of a fixed list (`alpha`, `beta`, `gamma`) in upper case followed by `!`. According to `README.md`, it is a small project whose file names contain spaces and non-ASCII characters, so it works as a test case for tooling that must handle such names.

## How it is structured

Three files, one job each: an entry script, a data provider and a text helper. The entry script depends on both helpers and the helpers depend on nothing. See `architecture.md` for the three zoom levels, `dependency-graph.md` for the import edges (no cycles), `mindmap.md` for the overview and `sequence-flow.md` for the one runtime flow.

## Key design choices

1. **Entry script wires everything.** `src/main.js` imports both helpers and runs the loop. Effect: all control flow is in one place. Reason: not stated in the code. <!-- codemap:unverified --> (inferred)
2. **Data behind a function.** `src/데이터 로더.js` keeps the array private and returns `items.slice()`, a copy. Effect: callers cannot mutate the stored list.
3. **Formatting in a utility module.** `src/my utils.js` exports `shout`, a pure function. Effect: it is easy to test on its own.
4. **CommonJS modules.** Files use `require` and `module.exports`; `package.json` has no `"type": "module"`. Effect: Node loads them as CommonJS.
5. **File names with a space and Hangul.** `src/my utils.js` and `src/데이터 로더.js` are required by exact name. `README.md` describes the project as one whose file names contain spaces and non-ASCII characters.

## Reading order (onboarding guide)

1. `README.md`: one-line purpose of the project.
2. `package.json`: the `main` field points to `src/main.js`.
3. `src/main.js`: the whole flow; note the two `require` lines and the loop.
4. `src/데이터 로더.js`: where the items come from and why a copy is returned.
5. `src/my utils.js`: what `shout` does to each item.

## Not covered

The repository was read completely; nothing was skipped.
