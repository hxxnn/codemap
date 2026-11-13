# relation-map Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `relation-map` skill (`/codemap relations`) whose HTML page shows project files as one full-screen graph, highlighting a file's direct neighbours on hover.

**Architecture:** The skill writes `relation-map.md` (file table = source of truth) and an HTML page holding a plain `<ul class="cm-graph">` data list. The shared `codemap.js` turns that list into an SVG graph (folder boxes, curved edges, hover/click focus, side panel, full screen). `check_output.py` validates the data and cross-checks it against the Markdown table.

**Tech Stack:** Python 3 + pytest (checker), vanilla JS/CSS (shared assets, no new library), Node + Playwright (`scripts/browser_check.js`).

**Spec:** `docs/superpowers/specs/2026-11-12-relation-map-design.md`

## Global Constraints
- No new external library or CDN resource; HTML pages keep exactly the shell's two `<script>` tags. Model-written HTML never contains `<script>`, event-handler attributes, `javascript:` URLs; all text is escaped.
- Relations come only from import/require/use statements actually read; highlight range is **direct (1-step) neighbours only**; no 2-step toggle.
- `skill: relation-map`; Markdown is the source, HTML its rendering. `sources:` stays a one-line `{path: sha256}` mapping. Footer section "다루지 않은 범위" is required.
- `/codemap all` becomes 7 skills; the default (no argument) set is unchanged. `--no-html` writes the Markdown only and says the interactive page was skipped.
- Groups start folded when the graph has **80 or more files**.
- Bump the first line of both shared assets to `/* codemap html assets v6 */` (same value in `codemap.css` and `codemap.js`).
- Output language Korean by default; skill instructions are English.
- Commits: `git add <files>` then `git -c user.name=hxxnn -c user.email=hxxnn@users.noreply.github.com commit -m "<msg>" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_01Kr6k6WyzMTXwQr5xPkAQBy"`. Work on branch `claude/tender-mayer-3bsfwd`; push after each task; never open a PR unless the user asks.
- Temporary files go in the scratchpad directory (`$SCRATCH`), never `/tmp`. Verify with `pytest scripts/tests -q` after every task.

## Review Focus
1. Graph with zero edges or a single file → the page shows an empty-state sentence, no JS error (Task 3).
2. Mutual import (A↔B) and self-import → edges drawn without overlap loops or hang; checker reports the self-edge (Tasks 1, 3).
3. Paths with spaces or Korean characters (`edge-names`) → ids, `data-group` and table parsing survive (Tasks 1, 3).
4. Same folder name at different depths (`a/utils`, `b/utils`) → groups keyed by the full path, not the last segment (Task 3).
5. 600-file graph and a hub with 100 neighbours → folded start, hover responds in under 100 ms, first layout under 3 s (Tasks 3, 4, 5).

## File Structure
- Create `skills/relation-map/SKILL.md`; `scripts/make_graph_fixture.py` (synthetic project generator for tests and perf).
- Modify `scripts/check_output.py` (+ `scripts/tests/test_check_output.py`, new `scripts/tests/test_make_graph_fixture.py`), `scripts/browser_check.js`, `skills/_shared/assets/codemap.js`, `skills/_shared/assets/codemap.css`, `skills/_shared/language-and-output.md`, `commands/codemap.md`, `scripts/tests/test_install_into_project.py`, `README.md`, `README.en.md`, `index.html`, `CLAUDE.md`, and `examples/*/docs/codemap/` (new files).

---

### Task 1: Checker for the relation-map Markdown and graph data

**Files:**
- Modify: `scripts/check_output.py` (constants at lines 17 and 22; new functions; `main`)
- Test: `scripts/tests/test_check_output.py`

**Interfaces:**
- Produces:
  - `parse_graph_html(text: str) -> list[dict]` — one dict per `ul.cm-graph > li`: `{"id": str, "group": str, "kind": str, "path": str, "uses": list[str]}` (`uses` = the `data-to` ids; `path` = text of the first `<code>`). Implement with `html.parser.HTMLParser`.
  - `parse_relation_table(md_text: str) -> dict[str, dict]` — first Markdown table whose rows start with a backticked path; columns by position: 1 path, 2 role, 3 uses, 4 used-by; maps path → `{"uses": list[str], "used_by": list[str]}` (cells hold backticked paths; `—` or empty = none).
  - `check_relation_graph(html_path, md_path, fixture_dir) -> list[str]` — problem strings.
  - `main` calls it when `<output_dir>/html/relation-map.html` exists; `NO_DIAGRAM_SKILLS` gains `"relation-map"`; `ARTIFACT_NAMES` gains `"relation-map.md"`.

- [ ] **Step 1: Write failing tests** in `scripts/tests/test_check_output.py`, using a helper `graph_html(nodes)` that renders `<ul class="cm-graph">` from `[(id, group, kind, path, [to_ids])]` and a helper `rel_md(rows)` that renders the 4-column table. One test per rule, asserting a substring of the problem:
  - `test_relation_graph_valid_passes` → `[]`
  - `test_relation_graph_dangling_edge_is_reported` → `"dangling"`
  - `test_relation_graph_duplicate_id_is_reported` → `"duplicate id"`
  - `test_relation_graph_self_edge_is_reported` → `"self"`
  - `test_relation_graph_ghost_node_path_is_reported` → `"does not exist"`
  - `test_relation_graph_bad_kind_or_missing_group_is_reported` → `"data-kind"` / `"data-group"`
  - `test_relation_graph_must_match_markdown_table` (edge in HTML absent from table) → `"mismatch"`
  - `test_relation_table_used_by_must_invert_uses` → `"used-by"`
  - `test_relation_graph_paths_with_spaces_and_korean_work` (path `src/내 파일 1.py`, fixture file exists) → `[]`
  - `test_relation_map_markdown_needs_no_diagram` (skill `relation-map`, no mermaid) → `check_file(...) == []`

- [ ] **Step 2: Run** `pytest scripts/tests/test_check_output.py -q -k relation` — Expected: FAIL (`AttributeError: ... no attribute 'check_relation_graph'`).

- [ ] **Step 3: Implement** the three functions and the constant changes above. Allowed `data-kind`: `source`, `test`, `unverified`. Reuse `_exists(rel, fixture_dir)` for path checks. Compare edges as sets of `(from_path, to_path)` between HTML and the table's `uses` columns.

- [ ] **Step 4: Run** `pytest scripts/tests -q` — Expected: all pass.

- [ ] **Step 5: Commit** — `git add scripts/check_output.py scripts/tests/test_check_output.py`, message `test: validate relation-map markdown and graph data`.

### Task 2: Synthetic project generator

**Files:**
- Create: `scripts/make_graph_fixture.py`
- Test: `scripts/tests/test_make_graph_fixture.py`

**Interfaces:**
- Consumes: `check_output.check_file`, `check_output.check_relation_graph`; `TEMPLATE` and `ASSETS` from `scripts/rebuild_example_html.py`.
- Produces: CLI `make_graph_fixture.py --nodes N --groups G --out DIR`, plus `build(nodes: int, groups: int, out: Path) -> None`. Writes a fake project under `DIR` (empty source files `pkg<g>/mod<i>.py`), `DIR/docs/codemap/relation-map.md`, `DIR/docs/codemap/html/relation-map.html` (shell filled from the template, language `ko`) and `html/assets/` copies. Graph shape, deterministic: node `i` in group `i % G`; node `i` uses `(i*7+1) % N` and `(i*13+5) % N` (skip self); node 0 is a hub used by every 5th node; every 10th node has kind `test`; node 3 has kind `unverified`; one mutual pair and one chain exist.

- [ ] **Step 1: Write failing test** `test_generated_fixture_passes_the_checker`: `build(12, 3, tmp)` then `check_output.main([str(tmp), str(tmp/"docs/codemap")]) == 0`; and `test_fixture_scales`: `build(600, 40, tmp)` completes and node count in the HTML equals 600.
- [ ] **Step 2: Run** `pytest scripts/tests/test_make_graph_fixture.py -q` — Expected: FAIL (module missing).
- [ ] **Step 3: Implement** `scripts/make_graph_fixture.py`. HTML content is the page sections: graph (`<ul class="cm-graph">`), file table, hubs, cycles, footer — the same data as the Markdown.
- [ ] **Step 4: Run** `pytest scripts/tests -q` — Expected: pass.
- [ ] **Step 5: Commit** — `git add scripts/make_graph_fixture.py scripts/tests/test_make_graph_fixture.py`, message `test: add synthetic graph fixture generator`.

### Task 3: Render the graph (layout, groups, folding, empty state)

**Files:**
- Modify: `skills/_shared/assets/codemap.js`, `skills/_shared/assets/codemap.css` (both: version line → v6), `scripts/browser_check.js`

**Interfaces:**
- Consumes: the fixture from Task 2.
- Produces: DOM contract used by Tasks 4–5. `buildGraph(ul)` wraps each `ul.cm-graph` in `figure.cm-graph-view` (toolbar `.cm-graph-tools`, stage `.cm-graph-stage` with `svg.cm-graph-svg`, panel `aside.cm-graph-panel`). SVG holds `g.cm-group[data-group]` (class `collapsed` when folded) containing `g.cm-node[data-id][data-kind]` (`tabindex="0"`, `role="button"`, `aria-label` = path) and `path.cm-edge[data-from][data-to]`; folded groups use `path.cm-edge.cm-agg[data-from-group][data-to-group]` with a count label. `layoutGraph(model) -> {groups, nodes}` is internal. The original `ul` stays in the DOM; CSS hides it on screen and shows it in `@media print` (and hides the figure in print).
- `browser_check.js` gains `--graph` mode.

- [ ] **Step 1: Write failing checks** in `browser_check.js` under `if (graph)` (flag `--graph`): `svg.cm-graph-svg` exists; `g.cm-node` count equals `ul.cm-graph > li` count; every `path.cm-edge` has both endpoints in the DOM; no node rectangles overlap (compare bounding boxes of nodes within one group); `ul.cm-graph` is not visible on screen; groups are keyed by full path (fixture includes `a/utils` and `b/utils` → two distinct `g.cm-group`); a graph with 80+ nodes starts with every group `collapsed` and shows `.cm-agg` edges, 79 nodes starts expanded. Add an empty-state check against a fixture with 1 node and 0 edges: the page contains an element `.cm-graph-empty` and no console error. Use a second generated fixture for each case (`--nodes 12 --groups 3`, `--nodes 100 --groups 8`, `--nodes 1 --groups 1`).
- [ ] **Step 2: Run** `python3 scripts/make_graph_fixture.py --nodes 12 --groups 3 --out $SCRATCH/fx12 && node scripts/browser_check.js $SCRATCH/fx12/docs/codemap/html/relation-map.html --graph` — Expected: FAIL ("svg.cm-graph-svg exists").
- [ ] **Step 3: Implement** `buildGraph` and `layoutGraph` in `codemap.js` (one IIFE section, after `upgradeTrees`) and styles in `codemap.css` using existing CSS tokens (`--canvas`, `--accent`, `--c-inferred`, `--c-cycle`, `--rule`). Layout: group boxes on a grid with `ceil(sqrt(groups))` columns ordered by path; files stacked vertically inside a box (row height 28 px); edges are cubic curves between box edges, drawn under nodes; mutual and self edges get a visible offset/loop. `unverified` nodes use a dashed outline, `test` nodes a distinct fill. Folded boxes show the folder name and file count; clicking a folded box expands it and recomputes layout. Zero nodes with edges → render `.cm-graph-empty` with a one-sentence Korean/English message (follow the existing `T` table) instead of an SVG.
- [ ] **Step 4: Run** the three browser checks and `pytest scripts/tests -q` — Expected: pass.
- [ ] **Step 5: Commit** — `git add skills/_shared/assets scripts/browser_check.js`, message `feat: render relation graph from a plain list`; push.

### Task 4: Hover, click-to-pin, keyboard/touch focus, side panel

**Files:**
- Modify: `skills/_shared/assets/codemap.js`, `skills/_shared/assets/codemap.css`, `scripts/browser_check.js`

**Interfaces:**
- Consumes: DOM contract from Task 3.
- Produces: `applyFocus(view, nodeId | null)` (internal) sets `is-focus` on the node, `is-uses` on files it imports, `is-usedby` on files importing it, `is-hot` on their connecting edges, and `is-dim` on every other node/edge; `null` clears all. Pinned state is stored as `data-pinned="<id>"` on the figure. Panel `.cm-graph-panel` lists path, role (the `<li>` text after `<code>`), "uses" and "used by" files as buttons that move focus to that node.

- [ ] **Step 1: Write failing checks** (`--graph`): on the 12-node fixture compute expected neighbours from the `ul` (direct only) and assert after hovering `g.cm-node[data-id="g1"]`: `.is-uses` set equals expected uses, `.is-usedby` set equals expected used-by, a 2-step neighbour is **not** highlighted, every other node has `is-dim`; moving the mouse away clears every state class; click pins (state persists after mouse leaves, `data-pinned` set), second click or `Escape` unpins; `Tab` focus + `Enter` behaves like click; the panel text lists the node's path; hovering the hub (node 0) on the 600-node fixture (groups expanded via a helper click) finishes in under 100 ms (`performance.now()` around dispatching `mouseover`); on the 100-node fixture hovering a folded group dims every group not connected to it; the mutual pair highlights each other.
- [ ] **Step 2: Run** the browser check on the 12-node fixture — Expected: FAIL (no `.is-uses`).
- [ ] **Step 3: Implement** with one delegated `mouseover`/`mouseout`/`click`/`focusin`/`keydown` listener on the figure (not one per node); neighbour lookup from precomputed `uses`/`usedBy` maps. Touch: a tap is a click (pin); no hover dependency. Respect `prefers-reduced-motion` (no transitions).
- [ ] **Step 4: Run** the browser checks and `pytest scripts/tests -q` — Expected: pass.
- [ ] **Step 5: Commit** — `git add skills/_shared/assets scripts/browser_check.js`, message `feat: highlight direct neighbours on hover, pin on click`; push.

### Task 5: Full screen, zoom, pan, theme and print

**Files:**
- Modify: `skills/_shared/assets/codemap.js`, `skills/_shared/assets/codemap.css`, `scripts/browser_check.js`

**Interfaces:**
- Consumes: DOM contract and `applyFocus` from Tasks 3–4.
- Produces: toolbar buttons `.cm-graph-zoom-in`, `.cm-graph-zoom-out`, `.cm-graph-fit`, `.cm-graph-fs`; class `cm-graph-full` on the figure while full screen; `toggleFullscreen(view)` (internal).

- [ ] **Step 1: Write failing checks** (`--graph`): clicking `.cm-graph-fs` makes the figure fill the viewport (bounding box equals viewport size) and sets `cm-graph-full`; `Escape` leaves it (and does not also unpin when full screen was active — first `Escape` exits full screen); the Fullscreen API being unavailable (stub `requestFullscreen` to reject) still gives the fixed-overlay fallback; zoom-in increases the SVG scale, fit restores it, dragging the stage moves the content; dark theme toggle keeps nodes visible (computed fill differs from background); print media (width 700) hides the figure and shows `ul.cm-graph`; the 600-node fixture's first layout completes in under 3 s (measure from navigation to `svg.cm-graph-svg` present).
- [ ] **Step 2: Run** the browser check — Expected: FAIL (no `.cm-graph-fs`).
- [ ] **Step 3: Implement** full screen (try `requestFullscreen()` on the figure, fall back to `position: fixed; inset: 0; z-index` class on rejection), zoom via SVG `viewBox`/transform with 0.4–3× limits like `setZoom`, drag-to-pan with pointer events, and `@media print` rules.
- [ ] **Step 4: Run** all `--graph` checks, `--deck` on an existing example page (regression), and `pytest scripts/tests -q` — Expected: pass.
- [ ] **Step 5: Commit** — `git add skills/_shared/assets scripts/browser_check.js`, message `feat: full-screen, zoom and pan for the relation graph`; push.

### Task 6: Skill, command routing and shared rules

**Files:**
- Create: `skills/relation-map/SKILL.md`
- Modify: `commands/codemap.md`, `skills/_shared/language-and-output.md`, `scripts/tests/test_install_into_project.py`

**Interfaces:**
- Consumes: data format and table columns from Tasks 1 and 3.
- Produces: skill name `relation-map`; argument `relations`.

- [ ] **Step 1: Write failing test** in `test_install_into_project.py`: `test_relation_map_skill_is_installed` — planned files include `.claude/skills/relation-map/SKILL.md`; and a test that `commands/codemap.md` mentions `relations` and the count of skills in `all` (7).
- [ ] **Step 2: Run** `pytest scripts/tests/test_install_into_project.py -q` — Expected: FAIL.
- [ ] **Step 3: Write `SKILL.md`** following `skills/dependency-graph/SKILL.md` and `skills/mindmap/SKILL.md`: front matter `name: relation-map` and an English `description`; Preflight and shared-rules reading; Method (read import statements of core source files, edges only from statements read, tests importing sources get kind `test`, dynamic imports → `unverified` with "(추정)"; assign `id`s `g1`…; `data-group` = the folder's full repo-relative path); Document layout (`# 파일 관계 지도`, file table with the four columns, hubs, cycles, footer); HTML section giving the exact `<ul class="cm-graph">` shape from the spec; Evidence rules; `--no-html` behaviour. Update `language-and-output.md`: add the `relation-map` row to "Where output goes" and a bullet in HTML step 2 describing `ul.cm-graph` (no `<script>`, never write SVG yourself). Update `commands/codemap.md`: `argument-hint` and description list `relations`; `all` = architecture, deps, mindmap, relations, sequence, doc, present; map `relations` → `relation-map`.
- [ ] **Step 4: Run** `pytest scripts/tests -q` and `claude plugin validate .` — Expected: pass (if the `claude` CLI is unavailable, say so and skip).
- [ ] **Step 5: Commit** — `git add skills/relation-map commands/codemap.md skills/_shared/language-and-output.md scripts/tests/test_install_into_project.py`, message `feat: add relation-map skill and /codemap relations`; push.

### Task 7: Real examples and model-compliance run

**Files:**
- Create: `examples/python-todo-api/docs/codemap/relation-map.md` and `html/relation-map.html`; same for `examples/ts-notes-cli` and `examples/edge-names`
- Modify: the existing examples' `html/assets/` (re-copied), possibly `sources` hashes via rerun

- [ ] **Step 1: Try a real run** per CLAUDE.md verification step 5: copy an example to `$SCRATCH/run-<name>`, delete its `docs/`, run `claude -p "/codemap relations" --plugin-dir /home/user/codemap --allowedTools "Read,Glob,Grep,Write,Edit,Bash(sha256sum:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(cp:*),Bash(find:*)"`, one project at a time. If `claude -p` is unavailable here, write the artifacts by following `SKILL.md` exactly and report that model compliance was **not** verified.
- [ ] **Step 2: Check** each result: `python3 scripts/check_output.py <project> <project>/docs/codemap --render` and `node scripts/browser_check.js <project>/docs/codemap/html/relation-map.html --graph` — Expected: exit 0. Include the `edge-names` project (paths with spaces/Korean).
- [ ] **Step 3: Rebuild** the other example pages with `python3 scripts/rebuild_example_html.py`, rerun the checker on all four examples and `node scripts/browser_check.js` on one page of each kind — Expected: exit 0; `git status` shows only intended files.
- [ ] **Step 4: Commit** — `git add examples`, message `docs: relation-map examples`; push.

### Task 8: Docs, gallery and final verification

**Files:**
- Modify: `README.md`, `README.en.md`, `index.html`, `CLAUDE.md`

- [ ] **Step 1: Update** READMEs (command list, `all` = 7, one-paragraph description of the interactive graph), `index.html` gallery (link the three new example pages, following the existing card pattern), and `CLAUDE.md` (structure section: new skill, shared graph DOM contract, `make_graph_fixture.py`; "현재 상태" and "다음 후보" refreshed; mention that `all` now has 7 skills and the 80-file fold rule).
- [ ] **Step 2: Run the full verification** from `CLAUDE.md`: `pytest scripts/tests -q`; `check_output.py` on every example; `browser_check.js` on one page per skill kind plus `--graph` on the fixtures and examples; `claude plugin validate .`.
- [ ] **Step 3: Report** which checks passed and which could not be run (model compliance, CDN-dependent renders), then commit `git add README.md README.en.md index.html CLAUDE.md` with message `docs: document relation-map`; push.
