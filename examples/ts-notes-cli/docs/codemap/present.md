---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: fabaf87a3aeb5141ee19be6283a4d4727a929ace6542da1e3da20eef52725ba0, docs/codemap/dependency-graph.md: 37de8c4b7a2765fed72da30bf7924d1c45e1ad42c27d048fc28b6812c6aacb0a, docs/codemap/mindmap.md: 5221fa8be8571bb10a223cc0fa7588328f199d0056142c1e646c672f4496743f, docs/codemap/sequence-flow.md: 94ed8888679da195a714b8251db773b141fd62b43e2cf91b62542ad81230d071, docs/codemap/design-doc.md: ac4e02f6d7f627732671b07d57d2d3cdae9d224114ae5b062aa32b465acc826e}
---

<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->


# Presentation outline

A 7-slide outline for `notes-cli`, built only from the other codemap artifacts. All five source artifacts were present.

## Slide 1: What it is
`notes-cli` is a small command-line notes tool written in TypeScript with no runtime dependencies. You add a note with `notes add` and print notes with `notes list`.
Show: `design-doc.md` → "Overview"

## Slide 2: The big picture
There is one container: a Node.js CLI process that keeps notes in memory. The only outside inputs are the terminal user and the `USER` environment variable.
Show: `architecture.md` → "Level 2: Containers" diagram

## Slide 3: How it is organized
Five files, five responsibilities: CLI, storage, identity, presentation and types.
Show: `mindmap.md` → the mindmap diagram

## Slide 4: How it runs
`notes add` looks up the user, then appends a note to the in-memory array; `notes list` formats each note and prints it.
Show: `sequence-flow.md` → "notes add" diagram

## Slide 5: How the parts depend on each other
Dependencies point one way, from the entry file down to the store, formatter and shared type. No circular dependencies were found.
Show: `dependency-graph.md` → the dependency flowchart and "Circular dependencies"

## Slide 6: Key design choices
Storage is in memory behind a small module, so notes are lost when the process exits. Command parsing lives in a single entry file; the reasons for these choices are inferred, not stated in the repo. <!-- codemap:unverified -->
Show: `design-doc.md` → "Key design choices"

## Slide 7: Where to start reading
Start with `README.md`, then `package.json`, `src/index.ts`, `src/notes-store.ts` and `src/types.ts`.
Show: `design-doc.md` → "Reading order (onboarding guide)"

## Not covered

Taken from the source artifacts: nothing was skipped; the whole repository was read. There are no tests and no dist/ folder in the repo.
