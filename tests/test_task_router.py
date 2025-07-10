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