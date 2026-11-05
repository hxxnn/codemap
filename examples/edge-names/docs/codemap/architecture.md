---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d, package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, README.md: 20617bb945b32699044b85affe89774ed9278ec9a9586b92f1528162c250eddc}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Architecture overview

`edge-names` is a tiny Node.js (CommonJS) program that prints a fixed list of items in upper case; this page shows it at three zoom levels.

## Level 1: System context

```mermaid
flowchart LR
  n1["Terminal user"]:::external
  n2["edge-names (src/main.js)"]
  n3["Standard output (console)"]:::external
  n1 -->|"runs node src/main.js"| n2
  n2 -->|"console.log"| n3
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

The system is one command-line program that writes to standard output; no database, network or other external service is referenced in the code.

## Level 2: Containers

```mermaid
flowchart LR
  n1["Terminal user"]:::external
  subgraph sys["edge-names"]
    n2["CLI script (Node.js, src/)"]
  end
  n3["Standard output (console)"]:::external
  n1 --> n2
  n2 --> n3
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

There is a single deployable part: the Node.js script in `src/`, started through `src/main.js` (`main` in `package.json`).

## Level 3: Components

```mermaid
flowchart TD
  subgraph entry["Entry point"]
    n1["main (src/main.js)"]
  end
  subgraph lib["Helpers"]
    n2["shout (src/my utils.js)"]
    n3["loadItems (src/데이터 로더.js)"]
  end
  n4["Standard output (console)"]:::external
  n1 -->|"loadItems()"| n3
  n1 -->|"shout(item)"| n2
  n1 -->|"console.log"| n4
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

`src/main.js` asks `src/데이터 로더.js` for the items, formats each with `src/my utils.js`, and prints the result.

## Not covered

The repository was read completely (3 source files, `package.json`, `README.md`); nothing was skipped.
