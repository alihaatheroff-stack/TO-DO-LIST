from datetime import datetime

todos = []
next_id = 1


def create_todo(title, description=""):
    global next_id

    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

    todo = {
        'id': next_id,
        'title': title.strip(),
        'description': description.strip(),
        'completed': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    todos.append(todo)
    next_id += 1
    return todo


def get_all_todos():
    return todos


def get_todo_by_id(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            return todo
    raise ValueError(f"Todo with id {todo_id} not found")


def update_todo(todo_id, title=None, description=None, completed=None):
    todo = get_todo_by_id(todo_id)

    if title is not None:
        if not title.strip():
            raise ValueError("Title cannot be empty")
        todo['title'] = title.strip()

    if description is not None:
        todo['description'] = description.strip()

    if completed is not None:
        todo['completed'] = completed

    return todo


def delete_todo(todo_id):
    global todos
    todo = get_todo_by_id(todo_id)
    todos = [t for t in todos if t['id'] != todo_id]
    return todo


def clear_all_todos():
    global todos, next_id
    todos = []
    next_id = 1