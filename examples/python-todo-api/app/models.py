from dataclasses import dataclass

from app import storage  # deliberate cycle: storage also imports models


@dataclass
class Todo:
    id: int
    title: str
    created_at: str
    done: bool = False

    def to_dict(self):
        return {"id": self.id, "title": self.title, "created_at": self.created_at, "done": self.done}

    @classmethod
    def create(cls, title, created_at):
        return cls(id=storage.next_id(), title=title, created_at=created_at)
