---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 8eca049d68973a1b7ac39eea77daca509e6ad1a05905d4f623f10b2b8e704d62, docs/codemap/dependency-graph.md: 3bb71e17ad5fe3cee22674e271c37e0ca2bd64bd076b498936e5f90b7b310941, docs/codemap/mindmap.md: 5243108c84621bb6d8f58083c9c3a5fdd5a9700e2457183b3afe168527c5a036, docs/codemap/sequence-flow.md: d8efe8e09a4a7166ee56cfb7408f4758aadd1b0126d5e609fa2c84205477e3b3, docs/codemap/design-doc.md: 7e5bf83f983afcbe7006c9b98bacbed5ad02168cafdde2c810ee1cc9244e43b1}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Presentation outline

A seven-slide walkthrough of `notes-cli`, built only from the existing codemap artifacts (all five were available).

## Slide 1: What it is
A small TypeScript command-line notes tool with two commands, `notes add` and `notes list`, running on Node.js with no runtime dependencies.
Show: `design-doc.md` → "Overview"

## Slide 2: The big picture
One Node.js process talks to the user's terminal and keeps its notes in an in-memory array inside the same process; there is no database.
Show: `architecture.md` → "Level 2: Containers" diagram

## Slide 3: How it is organized
Five small files, one responsibility each: CLI, storage, presentation, identity and types.
Show: `mindmap.md` → "Mindmap" diagram

## Slide 4: How it runs
`notes add` reads the user name, then stores a note; `notes list` formats every stored note and prints it.
Show: `sequence-flow.md` → "Scenario 1: `notes add <text>`" diagram

## Slide 5: How the parts depend on each other
Imports flow one way from `src/index.ts` down to `src/types.ts`, and there are no circular dependencies.
Show: `dependency-graph.md` → "Dependency graph" diagram and "Circular dependencies"

## Slide 6: Key design choices
Commands are parsed in a single entry file, and storage sits behind a small module with only `addNote` and `listNotes`. Notes are lost when the process ends; the reason for in-memory storage is a guess, not stated in the repository. (inferred) <!-- codemap:unverified -->
Show: `design-doc.md` → "Key design choices"

## Slide 7: Where to start reading
Start with `README.md`, then `package.json`, then `src/index.ts`, then `src/notes-store.ts`.
Show: `design-doc.md` → "Reading order (onboarding guide)"

## Not covered

Taken from the artifacts' own footers: all source files, `package.json` and `README.md` were read completely; `tsconfig.json` was only skimmed; there are no tests and no build output (`dist/`) in the repository.
