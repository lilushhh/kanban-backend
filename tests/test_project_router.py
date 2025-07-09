import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_projects_empty_or_existiong():
    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if data:
        for project in data:
            assert "name" in project
            assert "id" in project