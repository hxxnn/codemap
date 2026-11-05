---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Dependency graph: edge-names

## Internal imports

```mermaid
flowchart LR
  main["src/main.js"]
  utils["src/my utils.js"]
  loader["src/데이터 로더.js"]
  main -->|"require"| utils
  main -->|"require"| loader
```

`src/main.js` is the only file with imports: it requires both helper modules, and neither helper imports anything.

## Imports table

| File | Requires | Exports |
|---|---|---|
| `src/main.js` | `src/my utils.js`, `src/데이터 로더.js` | none |
| `src/my utils.js` | none | `shout` |
| `src/데이터 로더.js` | none | `loadItems` |

## Findings
- Circular dependencies: none.
- External (npm) packages: none; `package.json` has no `dependencies` field.
- Note: the `require` strings contain a space and Hangul characters (`./my utils.js`, `./데이터 로더.js`), which Node resolves as normal file names.

## Not covered
The whole repository was read; nothing was skipped.
