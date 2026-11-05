---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Mindmap

```mermaid
mindmap
  root((edge-names))
    n1["src/"]
      n2["main.js: entry, prints items"]
      n3["my utils.js: shout()"]
      n4["데이터 로더.js: loadItems()"]
    n5["package.json"]
```
The project is one entry file plus two helper modules.

## Not covered
The repo was read completely. `src/데이터 로더.js` is not listed in `sources` because its non-ASCII file name fails the safe-hashing rule (needs your decision).
