---
codemap: 1
skill: mindmap
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/types.ts: b0fbf687bc33cb22134e0f2fc8586140fa07017a3294fc7d8ce61dde9c83df62}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Mindmap

The `notes-cli` project at a glance, grouped by what the code does.

```mermaid
mindmap
  root((notes-cli))
    a1["CLI"]
      a2["src/index.ts: parses add / list"]
        a3["usage message and exit code 1"]
    a4["Storage"]
      a5["src/notes-store.ts: in-memory notes"]
        a6["addNote()"]
        a7["listNotes()"]
    a8["Presentation"]
      a9["src/format.ts: formats one note"]
        a10["formatNote()"]
    a11["Identity"]
      a12["src/user-profile.ts: current user"]
        a13["currentUser()"]
    a14["Types"]
      a15["src/types.ts: Note interface"]
```

The five source files split into five small responsibilities, one file each.

## Groups

- **CLI** — turns `notes add <text>` and `notes list` into calls; anything else prints a usage line and exits with 1.
- **Storage** — keeps notes in a module-level array and assigns ids as length + 1.
- **Presentation** — renders a note as `#id text (author)`.
- **Identity** — author name from the `USER` environment variable, falling back to `anonymous`.
- **Types** — the shared `Note` shape (`id`, `text`, `author`).

## Not covered

All source files were read completely; nothing was left out. `package.json`, `tsconfig.json` and `README.md` are configuration or docs and are not shown in the map.
