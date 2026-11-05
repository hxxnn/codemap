import { Note } from "./types";

export function formatNote(note: Note): string {
  return `#${note.id} ${note.text} (${note.author})`;
}
