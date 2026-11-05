---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Dependency graph

```mermaid
flowchart LR
  main["src/main.js"]
  utils["src/my utils.js"]
  loader["src/데이터 로더.js"]
  main -->|"require"| utils
  main -->|"require"| loader
```
Only `src/main.js` has imports; there are no circular dependencies and no third-party packages.

## Not covered
The repo was read completely. `src/데이터 로더.js` is not listed in `sources` because its non-ASCII file name fails the safe-hashing rule (needs your decision).
