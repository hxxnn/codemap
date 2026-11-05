# codemap Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `codemap` Claude Code plugin: seven instruction-only skills plus one entry command that read a codebase and produce Mermaid/HTML architecture documentation, installable from GitHub.

**Architecture:** The plugin is Markdown instructions (SKILL.md files) sharing three rule files under `skills/_shared/`. The only executable code is a dev-only Python checker (`scripts/check_output.py`) that mechanically verifies generated outputs against fixture repos. Skills are verified by running them on fixtures under `examples/` and passing the checker.

**Tech Stack:** Markdown skills/commands, JSON manifests, Python 3 + pytest (dev tooling only), `@mermaid-js/mermaid-cli` via `npx` (optional render check, dev only).

**Spec:** `docs/superpowers/specs/2026-11-05-codemap-design.md`

**Location:** a new directory `<repo-root>/` (the future GitHub repo root). All paths below are relative to it. Task 1 runs `git init` locally; creating the GitHub remote and pushing are done by the user, never by the executor.

## Global Constraints

- Plugin name `codemap`; entry command `/codemap`; install: `/plugin marketplace add <owner>/codemap` then `/plugin install codemap@codemap`.
- Seven skills, exactly: `architecture-overview`, `dependency-graph`, `mindmap`, `design-doc`, `sequence-flow`, `present`, `codemap-refresh`.
- Output goes to the target project's `docs/codemap/`; Mermaid Markdown is the default, HTML only when the user asks.
- Output language follows the user's request language; skill instructions themselves are written in English; README exists in English and Korean (`README.md`, `README.ko.md`).
- Unverified content is never stated as fact: it is labelled in the user's language and also carries the machine marker `<!-- codemap:unverified -->`.
- Nothing is overwritten in an existing `docs/codemap/` without asking the user first.
- No install step, runtime dependency, or script is required of plugin users.
- License: MIT (the spec left it open; decided here).

## Shared Contracts (decided here; every task relies on them)

- **Output files:** `docs/codemap/{architecture,dependency-graph,mindmap,sequence-flow,design-doc,present}.md`; HTML at `docs/codemap/html/<same-name>.html`.
- **Front matter on every generated file:**
  ```yaml
  ---
  codemap: 1
  skill: <skill name>
  generated_at: <ISO-8601 date>
  commit: <git HEAD sha or null>
  sources: {<relative/path>: <sha256 of file at generation>, ...}
  ---
  ```
  `sources` lists every file the artifact was derived from; `codemap-refresh` diffs against it.
- **Manual-edit zone:** text between `<!-- codemap:manual-start -->` and `<!-- codemap:manual-end -->` is never regenerated.
- **Project summary** (produced by `/codemap` step 1, handed to skills): bullet list with `languages`, `frameworks`, `entry_points`, `core_modules`, `external_systems`, `unread_scope`.
- Skills reference shared files by relative path `../_shared/<file>`.

## Review Focus

- Empty or doc-only repository → say there is nothing to map; produce no diagrams (Task 4, `examples/edge-empty`).
- Circular imports → shown and flagged, not looped forever or silently dropped (Task 6, python fixture).
- File names with hyphens/spaces/unicode inside Mermaid → quoted so the diagram still parses (Task 2 checker `--render`, Task 5).
- Existing `docs/codemap/` present → ask before overwrite; refresh keeps manual-edit zones (Tasks 4, 12).
- Repository too large to read fully → states the unread scope at the end of every artifact (Task 4 `unread_scope`, Task 9).

---

### Task 1: Repository scaffold and manifests

**Files:**
- Create: `codemap/.claude-plugin/plugin.json`, `codemap/.claude-plugin/marketplace.json`, `codemap/LICENSE`, `codemap/.gitignore`, `codemap/docs/design/codemap-design.md` (copy of the spec)

**Interfaces:**
- Produces: a valid plugin/marketplace manifest pair named `codemap`; later tasks add `commands/` and `skills/` beside it.

- [ ] **Step 1:** Ask the user for the display name to put in `author.name` / `owner.name` (public; do not use their email). Then `mkdir -p <repo-root> && cd <repo-root> && git init`.
- [ ] **Step 2:** Write `plugin.json` with `name: "codemap"`, `version: "0.1.0"`, a one-sentence `description` (maps a codebase into architecture diagrams, dependency graphs, mindmaps, sequence flows and an onboarding doc), and `author`.
- [ ] **Step 3:** Write `marketplace.json` with `name: "codemap"`, `owner`, and one plugin entry `{"name":"codemap","source":"./","description":<same>}`.
- [ ] **Step 4:** Add MIT `LICENSE` (year 2026, same display name), a `.gitignore` (`__pycache__/`, `node_modules/`, `.pytest_cache/`), and copy the spec into `docs/design/`.
- [ ] **Step 5: Verify** — Run: `for f in .claude-plugin/*.json; do python3 -m json.tool "$f" >/dev/null && echo ok $f; done`. Expected: `ok` for both files.
- [ ] **Step 6: Commit** — `git add -A && git commit -m "chore: scaffold codemap plugin manifests"`

### Task 2: Output checker (the only real code, TDD)

**Files:**
- Create: `scripts/check_output.py`, `scripts/tests/test_check_output.py`

**Interfaces:**
- Produces (in `scripts/check_output.py`):
  - `parse_front_matter(text: str) -> dict | None` — returns the parsed keys of the leading `---` block, or `None` if absent.
  - `mermaid_blocks(text: str) -> list[str]` — bodies of ```` ```mermaid ```` fences.
  - `path_refs(text: str) -> list[str]` — backtick-quoted tokens that contain `/` or end in a known source extension (`.py .ts .tsx .js .go .rs .java .md .json .toml`).
  - `check_file(md_path: Path, fixture_dir: Path) -> list[str]` — problem strings; empty list means pass. Rules: front matter present with keys `codemap, skill, generated_at, sources`; at least one mermaid block unless `skill` is `design-doc` or `present`; every path ref exists under `fixture_dir` unless its line contains `<!-- codemap:unverified -->`.
  - `main(argv: list[str]) -> int` — usage `check_output.py <fixture_dir> <output_dir> [--render]`; prints problems, returns 1 if any. `--render` additionally pipes each mermaid body through `npx -y @mermaid-js/mermaid-cli@11 -i - -o /dev/null` style rendering and reports failures.

- [ ] **Step 1: Write failing tests** in `test_check_output.py` using `tmp_path`:
  - `test_missing_front_matter_is_reported`: file without `---` header → problems contain `"front matter"`.
  - `test_nonexistent_path_is_reported`: front matter ok, mermaid block ok, text mentions `` `src/ghost.py` `` while fixture lacks it → problems contain `"src/ghost.py"`.
  - `test_unverified_line_may_reference_unknown_path`: same text but the line ends with `<!-- codemap:unverified -->` → `[]`.
  - `test_no_mermaid_block_fails_for_architecture`: `skill: architecture-overview`, no block → problems contain `"mermaid"`; same file with `skill: design-doc` → `[]`.
  - `test_valid_file_passes`: complete valid file → `[]`.
- [ ] **Step 2:** Run `python3 -m pytest scripts/tests -q`. Expected: FAIL (module not found).
- [ ] **Step 3:** Implement the functions above in `scripts/check_output.py` (stdlib only; parse front matter with a minimal `key: value` reader, no PyYAML).
- [ ] **Step 4:** Run `python3 -m pytest scripts/tests -q`. Expected: all pass.
- [ ] **Step 5: Commit** — `git add scripts && git commit -m "feat: add output checker for generated codemap files"`

### Task 3: Fixture repositories

**Files:**
- Create: `examples/python-todo-api/` (≈8 files: `app/main.py`, `app/routes.py`, `app/models.py`, `app/storage.py`, `app/utils.py`, `pyproject.toml`, `README.md`), `examples/ts-notes-cli/` (≈8 files incl. `src/user-profile.ts`, `src/index.ts`, `package.json`), `examples/edge-empty/README.md` only.

**Interfaces:**
- Produces: fixtures used by Tasks 4–12. Python fixture MUST contain one deliberate circular import (`models.py` ↔ `storage.py`) and one HTTP flow (`POST /todos` → `routes.py` → `storage.py`). TS fixture MUST contain a hyphenated filename and a CLI entry point (`src/index.ts`) calling two modules.

- [ ] **Step 1:** Create the three fixtures with small, realistic code (functions have real bodies; imports are real so dependency analysis has truth to find).
- [ ] **Step 2: Verify** — Run: `python3 -c "import ast,sys,pathlib; [ast.parse(p.read_text()) for p in pathlib.Path('examples/python-todo-api').rglob('*.py')]; print('ok')"`. Expected: `ok`.
- [ ] **Step 3: Commit** — `git add examples && git commit -m "test: add fixture repositories"`

### Task 4: Shared rules and the `/codemap` entry command

**Files:**
- Create: `skills/_shared/mermaid-rules.md`, `skills/_shared/language-and-output.md`, `commands/codemap.md`

**Interfaces:**
- Produces: the Shared Contracts above, written out as rules. `mermaid-rules.md`: allowed diagram types (`flowchart`, `mindmap`, `sequenceDiagram`, C4 expressed as flowcharts with subgraphs), quote every node label that contains `-`, space, `/`, `.` or non-ASCII, node cap (>30 nodes → group by folder), a pre-save checklist (balanced fences, no unquoted special chars, every id defined). `language-and-output.md`: language-follow rule, output paths, front matter, manual-edit zone, overwrite-confirmation rule, the unverified marker, the project-summary format, the "unread scope" footer.
- `commands/codemap.md` frontmatter: `description`, `argument-hint: "[all|architecture|deps|mindmap|sequence|doc|present|refresh] [--html]"`. Behaviour: (1) if the repo has no source files, say so and stop; (2) build the project summary; (3) if `docs/codemap/` exists, ask before regenerating (suggest `refresh`); (4) invoke the matching skill(s) — `all` means the six generators in order architecture, dependency, mindmap, sequence, doc, present; `refresh` means `codemap-refresh`.

- [ ] **Step 1:** Write the two shared files with the exact contents specified above.
- [ ] **Step 2:** Write `commands/codemap.md`.
- [ ] **Step 3: Verify** — Run Claude Code with the plugin loaded (`claude --plugin-dir <repo-root>`) inside `examples/edge-empty` and run `/codemap`. Expected: it reports there is nothing to map and writes no `docs/codemap/` directory (`test ! -d docs/codemap`).
- [ ] **Step 4: Commit** — `git add -A && git commit -m "feat: add shared rules and /codemap command"`

### Task 5: `architecture-overview` skill

**Files:**
- Create: `skills/architecture-overview/SKILL.md`

**Interfaces:**
- Consumes: project summary; `../_shared/mermaid-rules.md`, `../_shared/language-and-output.md`.
- Produces: `docs/codemap/architecture.md` with three levels, each its own mermaid block and one-sentence caption: (1) system context (users, external systems), (2) containers, (3) components of the most central container.

- [ ] **Step 1:** Write `SKILL.md`: frontmatter `name: architecture-overview` and a `description` that triggers on requests for architecture/overview/structure diagrams; body states the three levels, evidence rule (every box maps to a real path listed in `sources`), and marks anything inferred as unverified.
- [ ] **Step 2: Verify on both fixtures** — With the plugin loaded, run `/codemap architecture` in copies of `examples/python-todo-api` and `examples/ts-notes-cli`. Then: `python3 scripts/check_output.py <fixture> <fixture>/docs/codemap --render`. Expected: exit 0; the TS output renders despite `user-profile.ts` (quoted label).
- [ ] **Step 3: Commit** — `git add -A && git commit -m "feat: add architecture-overview skill"`

### Task 6: `dependency-graph` skill

**Files:**
- Create: `skills/dependency-graph/SKILL.md`

**Interfaces:**
- Produces: `docs/codemap/dependency-graph.md`: a flowchart of real imports; folder-grouped when >30 nodes; a "Circular dependencies" section listing each cycle, and cycle edges drawn with `==>` or a distinct linkStyle.

- [ ] **Step 1:** Write `SKILL.md` requiring edges to come from actual import/require statements read from files (not guessed from names).
- [ ] **Step 2: Verify** — Run `/codemap deps` on the python fixture, then the checker (`--render`). Expected: exit 0, and the output text names the `models.py` ↔ `storage.py` cycle (`grep -c "models" docs/codemap/dependency-graph.md` > 0 inside the cycle section).
- [ ] **Step 3: Commit** — `git add -A && git commit -m "feat: add dependency-graph skill"`

### Task 7: `mindmap` skill

**Files:**
- Create: `skills/mindmap/SKILL.md`

**Interfaces:**
- Produces: `docs/codemap/mindmap.md` with one Mermaid `mindmap`: root = project name, branches = top-level features/folders, depth ≤ 3.

- [ ] **Step 1:** Write `SKILL.md` (group by feature when folders do not reflect features; depth cap; quote rules from shared file).
- [ ] **Step 2: Verify** — Run `/codemap mindmap` on both fixtures; checker `--render` exits 0.
- [ ] **Step 3: Commit** — `git add -A && git commit -m "feat: add mindmap skill"`

### Task 8: `sequence-flow` skill

**Files:**
- Create: `skills/sequence-flow/SKILL.md`

**Interfaces:**
- Produces: `docs/codemap/sequence-flow.md`: 2–3 scenarios, each a `sequenceDiagram` whose participants are real modules; call steps not traceable in code are marked with a note and `<!-- codemap:unverified -->`. If the user names a scenario, use it; otherwise choose from entry points and say which were chosen and why.

- [ ] **Step 1:** Write `SKILL.md` accordingly.
- [ ] **Step 2: Verify** — Run `/codemap sequence` on the python fixture. Expected: a scenario for `POST /todos` whose participants are `routes` and `storage`; checker `--render` exits 0.
- [ ] **Step 3: Commit** — `git add -A && git commit -m "feat: add sequence-flow skill"`

### Task 9: `design-doc` skill

**Files:**
- Create: `skills/design-doc/SKILL.md`

**Interfaces:**
- Consumes: the generated architecture/deps/mindmap/sequence files when present (reads them; generates missing ones only after asking).
- Produces: `docs/codemap/design-doc.md` with sections: Overview, Key design choices, Reading order (onboarding: ordered list of real files with one line each), Not covered (the `unread_scope`). Design rationale without code evidence is labelled unverified, never asserted.

- [ ] **Step 1:** Write `SKILL.md`.
- [ ] **Step 2: Verify** — Run `/codemap doc` on the TS fixture, then the checker. Expected: exit 0; the doc ends with a "Not covered" section; every reading-order path exists (checker enforces).
- [ ] **Step 3: Commit** — `git add -A && git commit -m "feat: add design-doc skill"`

### Task 10: `present` skill

**Files:**
- Create: `skills/present/SKILL.md`

**Interfaces:**
- Consumes: existing artifacts only (no new code analysis).
- Produces: `docs/codemap/present.md`: 5–7 slides, each `## Slide N: <title>` + 1–2 sentences + which existing diagram to show (by file and heading). If required artifacts are missing, ask whether to generate them first.

- [ ] **Step 1:** Write `SKILL.md`.
- [ ] **Step 2: Verify** — Run `/codemap present` on the python fixture after running `all`. Expected: `grep -c '^## Slide' docs/codemap/present.md` prints 5, 6 or 7; checker exits 0. Run it on a fixture with no prior artifacts: it asks before generating.
- [ ] **Step 3: Commit** — `git add -A && git commit -m "feat: add present skill"`

### Task 11: HTML output (`--html`)

**Files:**
- Create: `skills/_shared/html-template.html`
- Modify: `skills/_shared/language-and-output.md` (HTML rules), each generator SKILL.md (one line: "if `--html`, also write the HTML version per shared rules")

**Interfaces:**
- Produces: a single self-contained HTML file with two placeholders, `{{TITLE}}` and `{{CONTENT}}`; Mermaid loaded from one CDN script pinned to an exact version at least two weeks old; light/dark via `prefers-color-scheme`; each diagram wrapped in a container with zoom/collapse controls and a search box that filters text sections.

- [ ] **Step 1:** Write the template and the HTML rules (file goes to `docs/codemap/html/<name>.html`; only on request).
- [ ] **Step 2: Verify** — Run `/codemap architecture --html` on the TS fixture and open the output with Playwright (`chromium.launch()`): assert no console errors and that at least one `svg` exists inside `.mermaid`. Expected: pass.
- [ ] **Step 3: Commit** — `git add -A && git commit -m "feat: add interactive HTML output"`

### Task 12: `codemap-refresh` skill

**Files:**
- Create: `skills/codemap-refresh/SKILL.md`

**Interfaces:**
- Consumes: front matter `sources` + `commit` of each file in `docs/codemap/`.
- Produces: regenerated artifacts only where a listed source changed, was deleted, or new top-level modules appeared; content between manual-edit markers preserved; a short report listing refreshed, unchanged, and conflicted files. No `docs/codemap/` → say nothing to refresh and suggest `/codemap`. Missing/old-format front matter → ask before full regeneration.

- [ ] **Step 1:** Write `SKILL.md` including the comparison procedure (recompute sha256 of each source, compare).
- [ ] **Step 2: Verify** — In a fixture copy with generated outputs: add a manual-edit block to `architecture.md`, edit `app/storage.py`, run `/codemap refresh`. Expected: `dependency-graph.md` and `architecture.md` refreshed, `mindmap.md` reported unchanged if its sources did not change, the manual block still present (`grep "codemap:manual-start"`), checker exits 0.
- [ ] **Step 3: Commit** — `git add -A && git commit -m "feat: add codemap-refresh skill"`

### Task 13: Examples, READMEs, install check

**Files:**
- Create: `README.md`, `README.ko.md`
- Modify: `examples/*/docs/codemap/` (commit the generated outputs from Tasks 5–12 for both non-empty fixtures)

**Interfaces:**
- Produces: install instructions (the two commands from Global Constraints), a feature list of the seven skills, links to the example outputs, and a note on how to edit the design (`html-template.html`, `mermaid-rules.md`, each `SKILL.md`).

- [ ] **Step 1:** Generate full outputs with `/codemap all --html` on both fixtures, run the checker with `--render` on each. Expected: exit 0 for both.
- [ ] **Step 2:** Write both READMEs; every command and path mentioned must exist.
- [ ] **Step 3: Install check** — In a clean Claude Code session: `/plugin marketplace add <repo-root>` then `/plugin install codemap@codemap`. Expected: the seven skills and `/codemap` are listed, and no skill named `_shared` appears.
- [ ] **Step 4:** Run `python3 -m pytest scripts/tests -q` once more. Expected: pass.
- [ ] **Step 5: Commit** — `git add -A && git commit -m "docs: add READMEs and example outputs"`
- [ ] **Step 6:** Tell the user the local repo is ready and give the commands to create the GitHub repository and push; do not run them.
