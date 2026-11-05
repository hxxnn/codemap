---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d, package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Mindmap

The whole project at a glance, grouped by what each file does.

```mermaid
mindmap
  root((edge-names))
    a1["Entry"]
      a2["src/main.js: prints each item"]
    a3["Data"]
      a4["src/데이터 로더.js: returns the items"]
        a5["loadItems()"]
    a6["Formatting"]
      a7["src/my utils.js: upper-case + !"]
        a8["shout()"]
```

Three groups, one file each; `src/main.js` ties the other two together.

## Groups

- **Entry** — `src/main.js` loops over the items and logs them.
- **Data** — `src/데이터 로더.js` holds the hard-coded list `alpha`, `beta`, `gamma` and returns a copy.
- **Formatting** — `src/my utils.js` upper-cases a string and appends `!`.

No minor items were left out.

## Not covered

Nothing was skipped; every file in the project was read.
