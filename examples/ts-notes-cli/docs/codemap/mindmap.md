---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {package.json: cabefc4d84df127d8c363c8a9257c3815a258930510b4de924fadf0ff55edfee, src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Mindmap

The `notes-cli` project at a glance, grouped by what each file does.

```mermaid
mindmap
  root((notes-cli))
    a1["CLI"]
      a2["src/index.ts: parses add / list"]
    a3["Storage"]
      a4["src/notes-store.ts: in-memory notes"]
        a5["addNote()"]
        a6["listNotes()"]
    a7["Presentation"]
      a8["src/format.ts: formats one note"]
        a9["formatNote()"]
    a10["Identity"]
      a11["src/user-profile.ts: author name"]
        a12["currentUser()"]
    a13["Types"]
      a14["src/types.ts: Note interface"]
```

Five groups, one per responsibility, each holding a single source file.

## Groups

- **CLI** — command-line entry that reads `add` or `list` and prints usage on anything else.
- **Storage** — keeps notes in a module-level array, so they last only for one process run.
- **Presentation** — turns a note into a line like `#1 text (author)`.
- **Identity** — returns the `USER` environment variable, or `anonymous`.
- **Types** — the shared `Note` shape (`id`, `text`, `author`).

Left out: `package.json`, `README.md` and `tsconfig.json` (project metadata, no logic).

## Not covered

The small repo was read completely except `tsconfig.json`, which was not opened.
