import { formatNote } from "./format";
import { Note } from "./types";

const notes: Note[] = [];

export function addNote(text: string, author: string): Note {
  const note = { id: notes.length + 1, text, author };
  notes.push(note);
  return note;
}

export function listNotes(): string[] {
  return notes.map(formatNote);
}
