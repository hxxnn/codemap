---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 909b01b2407810e88605d208577d203e42830720d57f7aa6fc45b448054a9698, docs/codemap/dependency-graph.md: 291b479a9d4ef0778d78742c57460ba5a1371a5a6a08c8712c28e96a77963e6d, docs/codemap/mindmap.md: dccc14b94f6e60422fd699c49c590d6aae03b93a3f2fc360a99790c721057c63, docs/codemap/sequence-flow.md: 15f76e01be5ce8ae4ea6c736344f7eda793d69921637462d6492cab330aa7978, docs/codemap/design-doc.md: 7d220d70cd33972a867f3341a0eed953137ccae5c7e6caa6c11c24600f3deeaf}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Presentation outline: edge-names

## Slide 1: What it is
A tiny Node.js CommonJS program (see `design-doc.md`).

## Slide 2: Structure
One entry file, `src/main.js`, and two helpers (see `architecture.md`).

## Slide 3: Dependencies
`src/main.js` requires both helpers. There are no cycles and no third-party packages (see `dependency-graph.md`).

## Slide 4: Runtime flow
Load the items, upper-case each one, and print it (see `sequence-flow.md`).

## Slide 5: The edge case
File names contain spaces and non-ASCII characters, and the imports use them exactly.

## Slide 6: Takeaways
The project is small and was read completely. Nothing in it is unverified except the design rationale.

## Not covered
Built only from the other codemap files. The repo itself was read completely.
