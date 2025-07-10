import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
from models.enums.status_enum import StatusEnum

client = TestClient(app)

def create_project():
    unique_name = f"Task Test Project {uuid4()}"
    payload = {
        "name_project": unique_name,
        "users_list": ["user1", "user2"]
    }
    response = client.post("/projects/", json=payload)
    assert response.status_code == 200
    return response.json()["id"]

def create_task(project_id):
    payload = {
        "project_id": project_id,
        "task_title": "Test Task For Get",
        "owners_list": ["user1"],
        "status_task": "todo"
    }
    res = client.post("/tasks/", json=payload)
    assert res.status_code == 200
    return res.json()["id"]

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

@pytest.mark.integration
def test_create_task_invalis_cases():
    fake_project_id = str(uuid4())
    payload_fake_id = {
        "project_id": fake_project_id,
        "task_title": "Task With Fake Project",
        "owners_list": ["user1"],
        "status_task": "todo"
    }
    res_fake_id = client.post("/tasks/", json=payload_fake_id)
    assert res_fake_id.status_code == 400
    assert res_fake_id.json()["detail"] == "cannot create task"

    real_project_id = create_project()
    payload_invalid_users = {
        "project_id": real_project_id,
        "task_title": "Task With Invalid Owners",
        "owners_list": ["not_in_project"],
        "status_task": "todo"
    }
    res_invalid_users = client.post("/tasks/", json=payload_invalid_users)
    assert res_invalid_users.status_code == 400
    assert res_invalid_users.json()["detail"] == "cannot create task"

    payload_missing_fields = {
        "project_id": real_project_id,
        "owners_list": ["user1"],
        "status_task": "todo"
    }
    res_missing_fields = client.post("/tasks/", json=payload_missing_fields)
    assert res_missing_fields.status_code == 422

@pytest.mark.integration
def test_get_task_by_valid_id():
    project_id = create_project()
    task_id = create_task(project_id)

    res = client.get(f"/tasks/{task_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == task_id
    assert data["text"] == "Test Task For Get"
    assert data["owners"] == ["user1"]
    assert data["status"] == "todo"