---
description: Map this codebase into architecture diagrams, a dependency graph, a structure tree (mindmap), sequence flows and an onboarding doc (Mermaid Markdown plus HTML).
argument-hint: "[all|architecture|deps|mindmap|sequence|doc|present|refresh] [--no-html]"
---

You are running the codemap workflow. Arguments: `$ARGUMENTS`

Everything you write during this workflow, in files and in chat messages, is in the output language defined in `language-and-output.md`: Korean unless the user explicitly asked for another language.

First read `${CLAUDE_PLUGIN_ROOT}/skills/_shared/language-and-output.md` and `${CLAUDE_PLUGIN_ROOT}/skills/_shared/mermaid-rules.md` and follow them for everything below.

1. **Preflight.** Run the Preflight in `language-and-output.md`: if there is no source code (only docs/config), say so, write nothing and stop.
2. **Choose the work** from the first argument (default `all`):
   - `all` → architecture, deps, mindmap, sequence, doc, present — in that order
   - `architecture` → skill `architecture-overview`; `deps` → `dependency-graph`; `mindmap` → `mindmap`; `sequence` → `sequence-flow`; `doc` → `design-doc`; `present` → `present`
   - `refresh` → skill `codemap-refresh` (skip step 3 and step 4)
   - Flags such as `--no-html` (or the legacy `--html`) are never the work argument: if the first argument is a flag, treat the work as `all`.
   - Anything else: show the usage line above and stop.
3. **Existing output?** If `docs/codemap/` already exists and the chosen work would write files in it, ask the user before continuing and suggest `refresh` as the non-destructive option.
4. **Build the project summary** as the Preflight describes and show it to the user in one short block.
4b. **HTML assets.** Unless `--no-html` was given, prepare `docs/codemap/html/assets/` once now, as step 0 of the HTML section in `language-and-output.md` describes, before running any skill.
5. **Run each chosen skill** in order, passing the project summary and the `--no-html` flag if present (HTML versions are written by default). After each, state which files were written.
6. Finish with a short list of the files written and anything marked unverified.
