import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_changes():
    resp = client.get("/api/changes/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_change_detail():
    resp = client.get("/api/changes/1")
    assert resp.status_code == 200
    data = resp.json()
    assert "diff" in data
    assert "ai_result" in data

def test_review_change():
    resp = client.post("/api/changes/1/review", json={"result": "通过", "comment": "同意上线"})
    assert resp.status_code == 200
    assert resp.json()["review_result"] == "通过" 