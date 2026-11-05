---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 65244941c9216c0d9ec17a4f16412cbca94d47d5a984ce52e2f44c954f2fdb1f, docs/codemap/dependency-graph.md: 83dfb3cc76426cf175db0d926f6b78c6592aa785e1c7c26e1ed8c7af296d4b3a, docs/codemap/mindmap.md: 4cd2ca6623fdc5bdfc4b7f3b9ead3eca670be36df5a042fe32af127d9e85c637, docs/codemap/sequence-flow.md: a6c50be6a75847a39133c7678a8617d4a14b6265c2716c1adfd72891b9f3108c, docs/codemap/design-doc.md: cffd45a673c4bc310b56c4a23a0840d08b1fdaf7b87906b583238295fc815e4c}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Presentation outline: notes-cli

A seven-slide walkthrough built from the five existing codemap artifacts; none were missing.

## Slide 1: What it is
`notes-cli` is a small command-line notes tool written in TypeScript on Node.js, with `notes add` and `notes list` commands.
Show: `design-doc.md` → "Overview"

## Slide 2: The big picture
The tool is a single Node.js process: a user runs a command and the process reads the `USER` environment variable to name the author.
Show: `architecture.md` → "Level 2: Containers" diagram

## Slide 3: How it is organized
Five small source files fall into five groups: CLI, Storage, Presentation, Identity and Types.
Show: `mindmap.md` → the mindmap diagram

## Slide 4: How it runs
For `notes add`, the entry file asks for the current user, then hands the text and author to the store.
Show: `sequence-flow.md` → "The add command" diagram

## Slide 5: How the parts depend on each other
Imports flow one way from `src/index.ts` down to `src/types.ts`, and no circular dependencies were found.
Show: `dependency-graph.md` → the flowchart and "Circular dependencies"

## Slide 6: Key design choices
Notes are kept in a module-level array, so they are not saved between runs. The reason for this is not stated in the code. (inferred) <!-- codemap:unverified -->
Command parsing is done by hand in the entry file, with a usage message and exit code 1 for unknown commands. The reason is not stated in the code. (inferred) <!-- codemap:unverified -->
Show: `design-doc.md` → "Key design choices"

## Slide 7: Where to start reading
Start with `README.md`, then `package.json`, then `src/index.ts` and `src/notes-store.ts`.
Show: `design-doc.md` → "Reading order (onboarding guide)"

## Not covered

The small repo was read completely except `tsconfig.json`, which was not opened. Nothing is vendored or generated, and no test files exist in the repo.
