---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Sequence flows

The project has one runtime path, so one scenario is traced; there is no storage, network or error handling to add a second or third.

## Running the script

The developer runs `node src/main.js`, the only entry point.

```mermaid
sequenceDiagram
  participant M as src/main.js
  participant L as src/데이터 로더.js
  participant U as src/my utils.js
  participant C as stdout
  M->>L: loadItems()
  L-->>M: copy of the items array
  loop for each item
    M->>U: shout(item)
    U-->>M: upper-cased text + "!"
    M->>C: console.log(...)
  end
```

The loader returns a copy of its three items, and the entry file formats and prints each one in turn.

1. Module load: `src/main.js` requires `shout` and `loadItems` (`src/main.js:require`).
2. `loadItems()` returns `items.slice()` (`src/데이터 로더.js:loadItems`).
3. For each item, `shout(item)` returns `text.toUpperCase() + "!"` (`src/my utils.js:shout`).
4. The result is printed with `console.log` (`src/main.js:console.log`).

## Not covered

Nothing was skipped; every function on the path was read. Output was derived from the code and the script was not executed.
