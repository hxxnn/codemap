---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Dependency graph

Each arrow points from the file that `require`s to the file it requires, based on the `require(...)` statements in the three source files.

```mermaid
flowchart LR
  n1["src/main.js"]
  n2["src/my utils.js"]
  n3["src/데이터 로더.js"]
  n1 --> n2
  n1 --> n3
```

`src/main.js` is the only importer; the two helper files import nothing.

## Circular dependencies

None found: `src/my utils.js` and `src/데이터 로더.js` contain no `require` statements, and there are no self-imports.

## Most depended-on files

- `src/my utils.js`: 1 incoming edge (from `src/main.js`)
- `src/데이터 로더.js`: 1 incoming edge (from `src/main.js`)

## Not covered

All source files were read completely; there are no dynamic imports. Nothing was skipped.
