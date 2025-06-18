#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

def test_database_sg_change():
    """
    测试数据库安全组变更的风险评估
    """
    
    # GitLab webhook 数据
    webhook_data = {
        "object_kind": "push",
        "event_name": "push",
        "before": "1234567890abcdef1234567890abcdef12345678",
        "after": "abcdefg1234567890abcdef1234567890abcdefg",
        "ref": "refs/heads/test/高风险---数据库安全组变更",
        "checkout_sha": "abcdefg1234567890abcdef1234567890abcdefg",
        "message": "test: 高风险 - 数据库安全组变更",
        "user_id": 1,
        "user_name": "test-automation",
        "user_username": "test-automation",
        "user_email": "test@example.com",
        "project_id": 1,
        "project": {
            "id": 1,
            "name": "risk-detection-test",
            "description": "Risk detection test project",
            "web_url": "http://gitlab.example.com/test/risk-detection-test",
            "avatar_url": None,
            "git_ssh_url": "git@gitlab.example.com:test/risk-detection-test.git",
            "git_http_url": "http://gitlab.example.com/test/risk-detection-test.git",
            "namespace": "test",
            "visibility_level": 0,
            "path_with_namespace": "test/risk-detection-test",
            "default_branch": "main",
            "homepage": "http://gitlab.example.com/test/risk-detection-test",
            "url": "git@gitlab.example.com:test/risk-detection-test.git",
            "ssh_url": "git@gitlab.example.com:test/risk-detection-test.git",
            "http_url": "http://gitlab.example.com/test/risk-detection-test.git"
        },
        "commits": [
            {
                "id": "abcdefg1234567890abcdef1234567890abcdefg",
                "message": "test: 高风险 - 数据库安全组变更\n\n- 新增内网MySQL访问规则\n- 修改SSH管理子网范围\n- 更新安全组标签配置",
                "title": "test: 高风险 - 数据库安全组变更",
                "timestamp": datetime.now().isoformat(),
                "url": "http://gitlab.example.com/test/risk-detection-test/-/commit/abcdefg1234567890abcdef1234567890abcdefg",
                "author": {
                    "name": "test-automation",
                    "email": "test@example.com"
                },
                "added": ["security/database-sg-rules.json"],
                "modified": [],
                "removed": []
            }
        ],
        "total_commits_count": 1,
        "push_options": {},
        "repository": {
            "name": "risk-detection-test",
            "url": "git@gitlab.example.com:test/risk-detection-test.git",
            "description": "Risk detection test project",
            "homepage": "http://gitlab.example.com/test/risk-detection-test",
            "git_http_url": "http://gitlab.example.com/test/risk-detection-test.git",
            "git_ssh_url": "git@gitlab.example.com:test/risk-detection-test.git",
            "visibility_level": 0
        }
    }
    
    # 发送到AI推理服务
    url = "http://localhost:8001/gitlab-webhook"
    headers = {
        "Content-Type": "application/json",
        "X-Gitlab-Event": "Push Hook"
    }
    
    try:
        print("发送数据库安全组变更测试数据到AI推理服务...")
        response = requests.post(url, json=webhook_data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("\n=== 风险评估结果 ===")
            print(f"风险等级: {result.get('risk_level', 'unknown')}")
            print(f"风险概率: {result.get('probability', 0.0):.2%}")
            print(f"处理状态: {result.get('status', 'unknown')}")
            
            if 'details' in result:
                print(f"\n详细信息: {result['details']}")
            
            print("\n=== Grafana仪表板验证 ===")
            print("请访问以下链接查看风险评估仪表板:")
            print("http://localhost:3000/Risk Assessment Dashboard")
            print("\n数据已成功存储到InfluxDB，可在Grafana中查看可视化结果")
            
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("连接失败：AI推理服务可能未运行，请检查服务状态")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    test_database_sg_change()