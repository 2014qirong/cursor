import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_users():
    resp = client.get("/api/user/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_login():
    resp = client.post("/api/user/login", json={"username": "admin", "password": "123456"})
    assert resp.status_code == 200
    assert "token" in resp.json() 