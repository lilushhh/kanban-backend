import pytest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4

client = TestClient(app)

@pytest.mark.integration
def test_read_projects_empty_or_existiong():
    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if data:
        for project in data:
            assert "name" in project
            assert "id" in project

@pytest.mark.integration
def test_get_project_by_valid_id():
    create_payload = {
        "name_project": "Project to get",
        "users_list": ["user1", "user2"]
    }

    create_response = client.post("/projects/", json=create_payload)
    assert create_response.status_code == 200

    created_project = create_response.json()
    project_id = created_project["id"]

    get_response = client.get(f"/projects/{project_id}")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["id"] == project_id
    assert data["name"] == "Project to get"
    assert data["users"] == ["user1", "user2"]

@pytest.mark.integration
def test_get_project_by_invalid_id():
    fake_id = str(uuid4())
    response = client.get(f"/projects/{fake_id}")
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "cannot find project"

@pytest.mark.integration
def test_create_project_success():
    payload = {
        "name_project": "Kanban Pytest Project",
        "users_list": ["user1", "user2"]
    }

    response = client.post("/projects/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Kanban Pytest Project"
    assert data["users"] == ["user1", "user2"]
    assert "id" in data 

@pytest.mark.integration
def test_create_project_missing_fields():
    payload = {
        "users_list": ["user1"]
    }
    response = client.post("/projects/", json=payload)
    assert response.status_code == 422

@pytest.mark.integration
def test_delete_existing_project():
    payload = {
        "name_project": "Project To Delete",
        "users_list": ["user1"]
    }

    create_response = client.post("/projects/", json=payload)
    assert create_response.status_code == 200

    created_project = create_response.json()
    project_id = created_project["id"]

    delete_response = client.delete(f"/projects/{project_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["message"] == "Project deleted successfully"

    get_response = client.get(f"/projects/{project_id}")
    assert get_response.status_code == 404

@pytest.mark.integration
def test_delete_non_existing_project():
    fake_id = str(uuid4())

    response = client.delete(f"/projects/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "cannot find project to delete"

@pytest.mark.integration
def test_update_existing_project():
    create_payload = {
        "name_project": "Project Before Update",
        "users_list": ["user1"]
    }
    create_response = client.post("/projects/", json=create_payload)
    assert create_response.status_code == 200

    created_project = create_response.json()
    project_id = created_project["id"]

    update_payload = {
        "project_id": project_id,
        "name_project": "Updated Project",
        "users_list": ["user1", "user2"]
    }
    update_response = client.put(f"/projects/{project_id}", json=update_payload)
    assert update_response.status_code == 200

    updated_data = update_response.json()
    assert updated_data["name"] == "Updated Project"
    assert updated_data["users"] == ["user1", "user2"]
    assert updated_data["id"] == project_id  

@pytest.mark.integration
def test_update_non_existing_project():
    fake_id = str(uuid4())

    update_payload = {
        "project_id": fake_id,
        "name_project": "Should Not Exist",
        "users_list": ["ghost"]
    }

    response = client.put(f"/projects/{fake_id}", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "project not found"