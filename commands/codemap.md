---
description: Map this codebase into architecture diagrams, a dependency graph, a mindmap, sequence flows and an onboarding doc (Mermaid Markdown, optional HTML).
argument-hint: "[all|architecture|deps|mindmap|sequence|doc|present|refresh] [--html]"
---

You are running the codemap workflow. Arguments: `$ARGUMENTS`

First read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/language-and-output.md` and `${CLAUDE_PLUGIN_ROOT}/skills/_shared/mermaid-rules.md` and follow them for everything below.

1. **Nothing to map?** If the current project has no source code files (only docs/config), tell the user in their language that there is nothing to map, produce no diagrams and no `docs/codemap/` directory, and stop.
2. **Choose the work** from the first argument (default `all`):
   - `all` → architecture, deps, mindmap, sequence, doc, present — in that order
   - `architecture` → skill `architecture-overview`; `deps` → `dependency-graph`; `mindmap` → `mindmap`; `sequence` → `sequence-flow`; `doc` → `design-doc`; `present` → `present`
   - `refresh` → skill `codemap-refresh` (skip step 3 and step 4)
   - Anything else: show the usage line above and stop.
3. **Existing output?** If `docs/codemap/` already exists and the chosen work would write files in it, ask the user before continuing and suggest `refresh` as the non-destructive option.
4. **Build the project summary** (format in `language-and-output.md`) by listing the folder tree, reading the manifest files (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, …), and locating entry points. Show it to the user in one short block.
5. **Run each chosen skill** in order, passing the project summary and the `--html` flag if present. After each, state which file was written.
6. Finish with a short list of the files written and anything marked unverified.
