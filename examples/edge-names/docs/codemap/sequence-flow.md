---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Sequence flow: edge-names

## Scenario: running the script

```mermaid
sequenceDiagram
  participant U as Person
  participant M as src/main.js
  participant L as src/데이터 로더.js
  participant S as src/my utils.js
  participant O as stdout
  U->>M: node src/main.js
  M->>S: require
  M->>L: require
  M->>L: loadItems()
  L-->>M: copy of alpha, beta, gamma
  loop each item
    M->>S: shout(item)
    S-->>M: upper-cased text plus "!"
    M->>O: console.log
  end
```

On start, `src/main.js` requires both helpers, loads the three items, and prints each one upper-cased with a trailing exclamation mark (ALPHA!, BETA!, GAMMA!).

## Not covered
The whole repository was read; the script was not executed, so the printed output is derived from reading the code.
