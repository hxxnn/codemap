---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 7cc23f53a6a47e3d9299a71692a3cb88d7441854f790b7800d79f9f704dada4a, docs/codemap/dependency-graph.md: 943773a88f52b60bf0b4f1deee69bf92efe6379f243b20f8a47d5792c36399a5, docs/codemap/mindmap.md: 44edf3b026b0c164ea8c1448781c15469f70776b791f686941cd10e2eb105722, docs/codemap/sequence-flow.md: fdc44442720286bc3f8c85bcfa109ea314b0cc209b29cab1d15c55367955ac34, docs/codemap/design-doc.md: c56c858068e798ff943343ffed8266ae0972632d825afd1e779603f5feab2bae}
---

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
