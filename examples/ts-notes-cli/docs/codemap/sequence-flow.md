---
codemap: 1
skill: sequence-flow
generated_at: 2026-11-05
commit: null
sources: {src/index.ts: be5d22e51faaa0dc869376308f53f8ca04a5edfa032fdf3d868567f5525ed53a, src/notes-store.ts: aad16c43600df721ab92215cc76da7c55e171174e4d37fb2ae5c9be4d49f5b69, src/format.ts: 2e6c72e3cdbd0da3428aec6ecdf22be5dfd5c63b01354323ed11473472a8ae26, src/user-profile.ts: 967091478d3e5ac4fc90ca6101539d92b9608550ade3c6a5517a19952bbd2993}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# Sequence flows

Three runtime scenarios traced from `src/index.ts`: the `add` command, the `list` command, and the unknown-command error path.

## The add command

The user runs `notes add <text>`.

```mermaid
sequenceDiagram
  participant U as User
  participant I as src/index.ts
  participant P as src/user-profile.ts
  participant S as src/notes-store.ts
  U->>I: notes add text
  I->>P: currentUser()
  P-->>I: USER or "anonymous"
  I->>S: addNote(text, author)
  S-->>I: Note (id, text, author)
```

The process then ends silently: `src/index.ts` ignores the returned note and prints nothing.

1. `src/index.ts` splits `process.argv` into `command` and `rest` and joins `rest` into the note text.
2. `src/user-profile.ts:currentUser` returns `process.env.USER ?? "anonymous"`.
3. `src/notes-store.ts:addNote` builds `{ id: notes.length + 1, text, author }` and pushes it onto the module-level array.

## The list command

The user runs `notes list`.

```mermaid
sequenceDiagram
  participant U as User
  participant I as src/index.ts
  participant S as src/notes-store.ts
  participant F as src/format.ts
  U->>I: notes list
  I->>S: listNotes()
  loop each stored note
    S->>F: formatNote(note)
    F-->>S: "#id text (author)"
  end
  S-->>I: string[]
  I-->>U: console.log per line
```

Because the array is created fresh in each process, a separate `notes list` run prints nothing.

1. `src/index.ts` matches `command === "list"`.
2. `src/notes-store.ts:listNotes` maps the array through `formatNote`.
3. `src/format.ts:formatNote` returns `` `#${note.id} ${note.text} (${note.author})` ``.
4. `src/index.ts` prints each line with `console.log`.

## Unknown command

The user runs `notes` with no command or an unrecognised one.

```mermaid
sequenceDiagram
  participant U as User
  participant I as src/index.ts
  U->>I: notes other
  alt command is neither add nor list
    I-->>U: stderr usage message
    I->>I: process.exit(1)
  end
```

The program writes the usage line to standard error and exits with code 1.

1. `src/index.ts` falls through to the final `else` branch.
2. It calls `console.error("usage: notes add <text> | notes list")` and then `process.exit(1)`.

## Not covered

The small repo was read completely except `tsconfig.json` and `src/types.ts` (a type-only interface with no runtime calls). No call in these flows was untraced.
