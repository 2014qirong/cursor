#!/usr/bin/env python3
import requests
import json

def test_clb_webhook():
    # CLB相关的测试数据
    data = {
        "object_kind": "push",
        "event_name": "push",
        "before": "abc123",
        "after": "def456",
        "ref": "refs/heads/main",
        "checkout_sha": "def456",
        "message": "Test commit",
        "user_id": 1,
        "user_name": "Test User",
        "user_username": "testuser",
        "user_email": "test@example.com",
        "user_avatar": "",
        "project_id": 123,
        "project": {
            "name": "test-project"
        },
        "commits": [
            {
                "id": "def456",
                "message": "Add CLB listener configuration with SSL certificate update",
                "author": {
                    "name": "Test User"
                },
                "added": ["clb_listener_change.json"],
                "modified": [],
                "removed": []
            }
        ],
        "total_commits_count": 1,
        "repository": {
            "name": "test-repo"
        }
    }
    
    # 发送请求
    try:
        response = requests.post('http://localhost:8001/gitlab-webhook', json=data)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("\n✅ CLB Webhook测试成功!")
            # 检查风险评估结果
            if result.get('risk_assessments'):
                risk = result['risk_assessments'][0]
                print(f"风险等级: {risk.get('risk_level')}")
                print(f"风险概率: {risk.get('probability')}")
                print(f"变更类型: {risk.get('change_type')}")
        else:
            print("❌ CLB Webhook测试失败!")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    test_clb_webhook()