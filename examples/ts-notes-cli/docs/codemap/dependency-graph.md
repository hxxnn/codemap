---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Dependency graph

Arrows point from the importing file to the file it imports, taken from the `import` statements in the five source files.

```mermaid
flowchart LR
  n1["src/index.ts"]
  n2["src/notes-store.ts"]
  n3["src/user-profile.ts"]
  n4["src/format.ts"]
  n5["src/types.ts"]
  n1 --> n2
  n1 --> n3
  n2 --> n4
  n2 --> n5
  n4 --> n5
```

The graph is a tree-like chain from the entry file `src/index.ts` down to `src/types.ts`, and `src/user-profile.ts` imports nothing from the project.

## Circular dependencies

None found: no file reaches itself through its imports, and there are no self-imports.

## Most depended-on files

- `src/types.ts` — imported by `src/notes-store.ts` and `src/format.ts` (2 incoming edges; it holds only the `Note` interface).
- `src/notes-store.ts` — imported by `src/index.ts` (1 incoming edge).
- `src/user-profile.ts` — imported by `src/index.ts` (1 incoming edge).
- `src/format.ts` — imported by `src/notes-store.ts` (1 incoming edge).

## Not covered

The small repo was read completely: every `.ts` file under `src/` was opened. Imports of built-in or third-party packages were ignored (none exist), and no dynamic imports were found.
