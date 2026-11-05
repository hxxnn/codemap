---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, README.md: ad3e9d59c7f90caab58f57655039b71b09108d4876e83a62570fdae41ee77e70, src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Architecture overview

`notes-cli` is a small TypeScript command-line notes tool (`package.json` declares the `notes` binary as build output `dist/index.js`), shown here at three zoom levels.

## Level 1: System context

```mermaid
flowchart LR
  u["Terminal user"]:::external
  env["Environment variable USER"]:::external
  sys["notes-cli (notes add / notes list)"]
  u -->|"runs commands"| sys
  env -->|"author name"| sys
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

A person runs `notes add` or `notes list` in a terminal, and the tool reads the `USER` environment variable (`src/user-profile.ts`) to name the author.

## Level 2: Containers

```mermaid
flowchart LR
  u["Terminal user"]:::external
  env["Environment variable USER"]:::external
  subgraph sys["notes-cli"]
    cli["CLI process (Node.js + TypeScript, src/)"]
  end
  u -->|"argv: add / list"| cli
  env -->|"process.env.USER"| cli
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

There is a single container: one Node.js process started from `src/index.ts`; notes live in a module-level array inside that process (`src/notes-store.ts`), so nothing is saved to disk or to a database and each run starts empty.

## Level 3: Components

```mermaid
flowchart LR
  subgraph entry["Entry"]
    idx["CLI entry (src/index.ts)"]
  end
  subgraph logic["Logic"]
    store["Notes store (src/notes-store.ts)"]
    fmt["Formatter (src/format.ts)"]
    prof["User profile (src/user-profile.ts)"]
  end
  subgraph shared["Shared"]
    types["Note type (src/types.ts)"]
  end
  env["Environment variable USER"]:::external
  idx -->|"addNote, listNotes"| store
  idx -->|"currentUser"| prof
  store -->|"formatNote"| fmt
  store -->|"Note"| types
  fmt -->|"Note"| types
  env -->|"read"| prof
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

`src/index.ts` parses the command and delegates to the store and the user profile, while the store uses the formatter to turn notes into display lines and all three share the `Note` interface.

## Not covered

The small repo was read completely, except `tsconfig.json`, which was not opened, so compiler settings are not described. Nothing is vendored, and the build output folder dist/ does not exist in the repo.
