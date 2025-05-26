import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_send_notify():
    resp = client.post("/api/notify/", json={"to": "user1", "content": "测试消息"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "sent" 