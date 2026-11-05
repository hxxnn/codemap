---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Sequence flow: `node src/main.js`

```mermaid
sequenceDiagram
  participant M as src/main.js
  participant L as src/데이터 로더.js
  participant U as src/my utils.js
  M->>L: loadItems()
  L-->>M: copy of the items list
  loop each item
    M->>U: shout(item)
    U-->>M: upper-cased text plus "!"
    M->>M: console.log(result)
  end
```
Items are loaded once, then each one is upper-cased and printed, giving `ALPHA!`, `BETA!`, `GAMMA!`.

## Not covered
The repo was read completely. `src/데이터 로더.js` is not listed in `sources` because its non-ASCII file name fails the safe-hashing rule (needs your decision).
