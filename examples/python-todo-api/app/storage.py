from app import models  # deliberate cycle: models also imports storage

_TODOS = []


def next_id():
    return len(_TODOS) + 1


def add_todo(title, created_at):
    todo = models.Todo.create(title, created_at)
    _TODOS.append(todo)
    return todo


def all_todos():
    return list(_TODOS)
