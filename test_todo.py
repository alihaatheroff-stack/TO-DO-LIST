import pytest
import todo
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_todos():
    todo.clear_all_todos()


class TestCreateTodo:
    def test_create_todo_successfully(self):
        result = todo.create_todo("Buy groceries", "Milk and eggs")
        assert result['title'] == "Buy groceries"
        assert result['description'] == "Milk and eggs"
        assert result['completed'] == False
        assert result['id'] == 1

    def test_create_todo_empty_title_fails(self):
        with pytest.raises(ValueError) as error:
            todo.create_todo("")
        assert "empty" in str(error.value)

    def test_create_multiple_todos_get_unique_ids(self):
        first = todo.create_todo("First task")
        second = todo.create_todo("Second task")
        assert first['id'] != second['id']


class TestGetTodos:
    def test_get_all_empty(self):
        result = todo.get_all_todos()
        assert result == []

    def test_get_all_returns_all(self):
        todo.create_todo("Task 1")
        todo.create_todo("Task 2")
        result = todo.get_all_todos()
        assert len(result) == 2

    def test_get_by_id_success(self):
        created = todo.create_todo("Test task")
        found = todo.get_todo_by_id(created['id'])
        assert found['title'] == "Test task"

    def test_get_by_id_not_found(self):
        with pytest.raises(ValueError) as error:
            todo.get_todo_by_id(999)
        assert "not found" in str(error.value)


class TestUpdateTodo:
    def test_update_title(self):
        created = todo.create_todo("Old title")
        updated = todo.update_todo(created['id'], title="New title")
        assert updated['title'] == "New title"

    def test_mark_as_completed(self):
        created = todo.create_todo("Task")
        updated = todo.update_todo(created['id'], completed=True)
        assert updated['completed'] == True

    def test_update_nonexistent_todo(self):
        with pytest.raises(ValueError):
            todo.update_todo(999, title="New title")


class TestDeleteTodo:
    def test_delete_success(self):
        created = todo.create_todo("Task to delete")
        todo.delete_todo(created['id'])
        assert len(todo.get_all_todos()) == 0

    def test_delete_nonexistent_todo(self):
        with pytest.raises(ValueError):
            todo.delete_todo(999)


class TestAPIEndpoints:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()['status'] == "healthy"

    def test_create_todo_api(self):
        response = client.post("/todos", json={
            "title": "Test todo",
            "description": "Test description"
        })
        assert response.status_code == 201
        assert response.json()['title'] == "Test todo"

    def test_get_all_todos_api(self):
        client.post("/todos", json={"title": "Task 1"})
        client.post("/todos", json={"title": "Task 2"})
        response = client.get("/todos")
        assert response.status_code == 200
        assert response.json()['count'] == 2

    def test_delete_todo_api(self):
        created = client.post("/todos", json={"title": "Task"})
        todo_id = created.json()['id']
        response = client.delete(f"/todos/{todo_id}")
        assert response.status_code == 200