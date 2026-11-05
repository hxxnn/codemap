---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Architecture: edge-names

## Level 1 — System context

```mermaid
flowchart LR
  user["Person running node"]
  app["edge-names (CLI script)"]
  out["Standard output (terminal)"]
  user --> app
  app --> out
```

A person runs the script with Node.js and it prints one line per item to standard output. It uses no database, network or other external system.

## Level 2 — Containers

```mermaid
flowchart TD
  subgraph proc["Single Node.js process"]
    src["src/ (3 CommonJS files)"]
  end
  pkg["package.json (main: src/main.js)"]
  pkg --> src
```

The project is one Node.js process whose entry point is declared in `package.json` as `src/main.js`.

## Level 3 — Components

```mermaid
flowchart TD
  main["src/main.js (entry, prints results)"]
  utils["src/my utils.js (shout)"]
  loader["src/데이터 로더.js (loadItems)"]
  main --> utils
  main --> loader
```

`src/main.js` loads items through `loadItems` in `src/데이터 로더.js` and formats each one through `shout` in `src/my utils.js`.

## Not covered
The whole repository (4 source/manifest files) was read; nothing was skipped.
