---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Sequence flows

The program has one runtime scenario, so a single flow is shown: running the script.

## Run `node src/main.js`

The user starts the script from a terminal; it loads the items and prints each one shouted.

```mermaid
sequenceDiagram
  participant U as Terminal user
  participant M as src/main.js
  participant L as src/데이터 로더.js
  participant S as src/my utils.js
  participant O as stdout
  U->>M: node src/main.js
  M->>L: loadItems()
  L-->>M: copy of ["alpha","beta","gamma"]
  loop for each item
    M->>S: shout(item)
    S-->>M: item upper-cased + "!"
    M->>O: console.log(result)
  end
```

1. Module load: `src/main.js` requires `shout` and `loadItems` (`src/main.js:require`).
2. `loadItems()` returns `items.slice()` (`src/데이터 로더.js:loadItems`).
3. For each item, `shout(item)` returns `text.toUpperCase() + "!"` (`src/my utils.js:shout`).
4. `console.log` prints `ALPHA!`, `BETA!`, `GAMMA!` (`src/main.js:console.log`).

## Not covered

The repository was read completely. Only one scenario exists; there is no error handling or other branch in the code.
