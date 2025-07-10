import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from models.enums.status_enum import StatusEnum

client = TestClient(app)

def create_project():
    payload = {
        "name_project": "Task Test Project",
        "users_list": ["user1", "user2"]
    }
    response = client.post("/projects/", json=payload)
    assert response.status_code == 200
    return response.json()["id"]

@pytest.mark.integration
def test_create_task_success():
    project_id = create_project()
    payload = {
        "project_id": project_id,
        "task_title": "Test Task 1",
        "owners_list": ["user1"],
        "status_task": "todo"
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test Task 1"
    assert data["owners"] == ["user1"]
    assert data["status"] == "todo"
    assert data["project_id"] == project_id
    assert "id" in data