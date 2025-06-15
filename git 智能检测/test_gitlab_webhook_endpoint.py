#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_gitlab_webhook_endpoint():
    """测试 GitLab Webhook 端点"""
    
    # GitLab Push Event 测试数据
    webhook_payload = {
        "object_kind": "push",
        "event_name": "push",
        "before": "95790bf891e76fee5e1747ab589903a6a1f80f22",
        "after": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
        "ref": "refs/heads/master",
        "checkout_sha": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
        "user_id": 4,
        "user_name": "John Smith",
        "user_username": "jsmith",
        "user_email": "john@example.com",
        "project_id": 15,
        "project": {
            "id": 15,
            "name": "Diaspora",
            "description": "",
            "web_url": "http://example.com/mike/diaspora",
            "avatar_url": None,
            "git_ssh_url": "git@example.com:mike/diaspora.git",
            "git_http_url": "http://example.com/mike/diaspora.git",
            "namespace": "Mike",
            "visibility_level": 0,
            "path_with_namespace": "mike/diaspora",
            "default_branch": "master",
            "homepage": "http://example.com/mike/diaspora",
            "url": "git@example.com:mike/diaspora.git",
            "ssh_url": "git@example.com:mike/diaspora.git",
            "http_url": "http://example.com/mike/diaspora.git"
        },
        "commits": [
            {
                "id": "b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
                "message": "Update NodePool configuration for production cluster\n\nkind: NodePool\napiVersion: infrastructure.cluster.x-k8s.io/v1beta1\nmetadata:\n  name: worker-nodepool\nspec:\n  replicas: 5",
                "title": "Update NodePool configuration for production cluster",
                "timestamp": "2012-01-03T23:36:29+02:00",
                "url": "http://example.com/mike/diaspora/commit/b6568db1bc1dcd7f8b4d5a946b0b91f9dacd7327",
                "author": {
                    "name": "John Smith",
                    "email": "john@example.com"
                },
                "added": ["CHANGELOG"],
                "modified": ["app/controller/application.rb"],
                "removed": []
            },
            {
                "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
                "message": "Add new OSS bucket permissions for data processing\n\nGrant read/write access to oss://data-processing-bucket/*",
                "title": "Add new OSS bucket permissions for data processing",
                "timestamp": "2012-01-03T23:37:29+02:00",
                "url": "http://example.com/mike/diaspora/commit/da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
                "author": {
                    "name": "John Smith",
                    "email": "john@example.com"
                },
                "added": ["CHANGELOG"],
                "modified": ["config/oss-policy.json"],
                "removed": []
            }
        ],
        "total_commits_count": 2,
        "repository": {
            "name": "Diaspora",
            "url": "git@example.com:mike/diaspora.git",
            "description": "",
            "homepage": "http://example.com/mike/diaspora",
            "git_http_url": "http://example.com/mike/diaspora.git",
            "git_ssh_url": "git@example.com:mike/diaspora.git",
            "visibility_level": 0
        }
    }
    
    # 测试不同的端口
    test_ports = [8001, 8002, 8000]
    
    for port in test_ports:
        url = f"http://127.0.0.1:{port}/gitlab-webhook"
        print(f"\n=== 测试端口 {port} ===")
        
        try:
            # 发送 POST 请求
            response = requests.post(
                url,
                json=webhook_payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                print("✅ GitLab Webhook 测试成功！")
                return True
            else:
                print(f"❌ 请求失败，状态码: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 无法连接到端口 {port}")
        except requests.exceptions.Timeout:
            print(f"❌ 请求超时")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    print("\n❌ 所有端口测试失败")
    return False

def test_health_endpoint():
    """测试健康检查端点"""
    test_ports = [8001, 8002, 8000]
    
    for port in test_ports:
        url = f"http://127.0.0.1:{port}/health"
        print(f"\n=== 测试健康检查端口 {port} ===")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                print("✅ 健康检查成功！")
                return True
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 无法连接到端口 {port}")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    return False

if __name__ == '__main__':
    print("=== GitLab Webhook 端点测试 ===")
    
    # 先测试健康检查
    if test_health_endpoint():
        print("\n服务运行正常，开始测试 GitLab Webhook...")
        test_gitlab_webhook_endpoint()
    else:
        print("\n❌ 服务未运行，请先启动 AI 推理服务")
        print("启动命令: python3 -m uvicorn ai_infer_service.main:app --host 127.0.0.1 --port 8001")