---
codemap: 1
skill: present
generated_at: 2026-11-05
commit: null
sources: {docs/codemap/architecture.md: 1d913ac79b8c246c8953950089a111b8fcbcb9f308b1ed2d9d90e2b1bf5f0d6b, docs/codemap/dependency-graph.md: 092f5354fdffc5909503b5d5039a406d2c49f0207db94c256994e2e832dd84a0, docs/codemap/mindmap.md: 310e0b8f312fe690a6034bb023c5d95d9ccf06a3c97a945d8bb338715640f52a, docs/codemap/sequence-flow.md: ab6917491e31ef924747c353d75e8e53342eaaa28b7bea99f4994a9faac820d4, docs/codemap/design-doc.md: a3216b28b66b989b44f45f4d716324b9f87ef097f308d3f92e4d19837097b38c}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Presentation outline

A 7-slide walkthrough of `edge-names`, built only from the existing codemap artifacts (none were missing).

## Slide 1: What it is
A tiny Node.js script that prints three upper-cased words. Its README says its purpose is to have file names with spaces and non-ASCII characters.
Show: `design-doc.md` → "Overview"

## Slide 2: The big picture
One container, a CLI script, run by a developer and printing to the terminal.
Show: `architecture.md` → "Containers" diagram

## Slide 3: How it is organized
Three files in three groups: entry, data and formatting.
Show: `mindmap.md` → "Mindmap" diagram

## Slide 4: How it runs
The entry file loads the items once, then formats and prints each one in a loop.
Show: `sequence-flow.md` → "Running the script" diagram

## Slide 5: How the parts depend on each other
Only `src/main.js` imports anything, and there are no circular dependencies.
Show: `dependency-graph.md` → "Dependency graph" diagram

## Slide 6: Key design choices
The entry file wires everything, so the helper modules stay independent. The data module returns a copy of its list; the reason for the copy is inferred. <!-- codemap:unverified -->
Show: `design-doc.md` → "Key design choices"

## Slide 7: Where to start reading
Read `README.md`, then `package.json`, then `src/main.js`, then `src/데이터 로더.js`.
Show: `design-doc.md` → "Reading order (onboarding guide)"

## Not covered

Taken from the artifacts' own footers: nothing was skipped; all source files, `package.json` and `README.md` were read. The script was not executed, and the project has no tests.
