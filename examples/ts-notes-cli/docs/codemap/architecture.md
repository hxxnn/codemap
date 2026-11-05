---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62, package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, tsconfig.json: fbfb5e54f48dbca20aff45f6530b732e22d3c4fd596d106e199b9ee5ff9eb439, README.md: ad3e9d59c7f90caab58f57655039b71b09108d4876e83a62570fdae41ee77e70}
---

<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->


# Architecture overview

`notes-cli` is a small TypeScript command-line notes tool, shown here at three zoom levels.

## Level 1: System context

```mermaid
flowchart LR
  user["Terminal user"]
  sys["notes-cli (notes command)"]
  env["USER environment variable"]
  out["stdout / stderr"]
  user -->|"notes add / notes list"| sys
  env -->|"author name"| sys
  sys -->|"formatted notes, usage errors"| out
```

The user runs the `notes` command; the tool reads the author from the `USER` environment variable and prints to the terminal.

## Level 2: Containers

```mermaid
flowchart LR
  user["Terminal user"]
  cli["CLI process (Node.js, TypeScript) src/ built to dist/index.js"]
  mem["In-memory note array (inside the CLI process)"]
  user --> cli
  cli --> mem
```

There is a single container, the Node.js CLI process (`bin` in `package.json`); notes live only in that process's memory, with no database or file storage.

## Level 3: Components

```mermaid
flowchart TD
  subgraph entry["Entry layer"]
    idx["CLI entry (src/index.ts)"]
  end
  subgraph logic["Logic layer"]
    store["Notes store (src/notes-store.ts)"]
    prof["User profile (src/user-profile.ts)"]
    fmt["Formatter (src/format.ts)"]
  end
  subgraph shared["Shared types"]
    types["Note interface (src/types.ts)"]
  end
  idx --> store
  idx --> prof
  store --> fmt
  store --> types
  fmt --> types
```

`src/index.ts` parses the command and delegates to `src/notes-store.ts` and `src/user-profile.ts`; the store uses `src/format.ts` for output, and both share the `Note` type from `src/types.ts`.

## Notes

- The notes array is a module-level variable in `src/notes-store.ts`, so notes do not survive between runs of the command.

## Not covered

Nothing was skipped: all five files under `src/` plus `package.json`, `tsconfig.json` and `README.md` were read. The build output folder dist/ does not exist in the repo.
