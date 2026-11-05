---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c, src/데이터 로더.js: 992b2fa3a7a70e6fa9d036713db3edf2e7a7b7c1c67cae7bd75e74a31791473d, package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, README.md: 20617bb945b32699044b85affe89774ed9278ec9a9586b92f1528162c250eddc}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Architecture overview

`edge-names` is a tiny Node.js command-line script that loads three items, upper-cases them and prints them.

## System context

```mermaid
flowchart LR
  u["Developer running node"]:::external
  s["edge-names (package.json)"]
  o["Terminal stdout"]:::external
  u -->|"runs src/main.js"| s
  s -->|"prints lines"| o
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

The only things around the system are the person who runs `src/main.js` and the terminal that receives the output; no database or network call appears in the code.

## Containers

```mermaid
flowchart LR
  u["Developer"]:::external
  subgraph sys["edge-names"]
    cli["CLI script: Node.js (src/)"]
  end
  o["Terminal stdout"]:::external
  u --> cli
  cli --> o
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

There is a single container: one Node.js script whose entry point is `src/main.js`, as declared by `main` in `package.json`.

## Components

```mermaid
flowchart LR
  subgraph app["src/"]
    main["Entry: src/main.js"]
    utils["Formatter: src/my utils.js"]
    loader["Data source: src/데이터 로더.js"]
  end
  o["Terminal stdout"]:::external
  main -->|"loadItems()"| loader
  main -->|"shout()"| utils
  main -->|"console.log"| o
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

`src/main.js` pulls the items from `src/데이터 로더.js`, formats each with `src/my utils.js` and prints the result.

## Not covered

Nothing was skipped: all three source files, `package.json` and `README.md` were read in full. There is no build output, vendored code or test folder.
