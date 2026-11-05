---
codemap: 1
skill: dependency-graph
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---

# Dependency graph

Which source file imports which, taken from the `import` statements in `src/`.

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

Arrows point from the importing file to the imported file; `src/user-profile.ts` imports nothing from the project.

## Circular dependencies

None found. All five files form an acyclic graph.

## Most depended-on files

- `src/types.ts`: imported by `src/notes-store.ts` and `src/format.ts` (2 incoming edges).
- `src/notes-store.ts`: imported by `src/index.ts` (1).
- `src/format.ts`: imported by `src/notes-store.ts` (1).
- `src/user-profile.ts`: imported by `src/index.ts` (1).

## Not covered

Nothing was skipped; every file under `src/` was read. Imports of third-party packages: none exist (only Node's global `process` is used).
