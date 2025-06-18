#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的API测试脚本
"""

import requests
import json

def test_predict_api():
    """测试预测API"""
    print("🔍 测试AI预测API...")
    
    test_data = {
        "code": "# 数据库连接池配置\npool:\n  max_connections: 50\n  min_idle_connections: 10\n  connection_timeout: 20s\n  idle_timeout: 600s\n  max_lifetime: 2h"
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/predict",
            json=test_data,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API测试成功!")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return True
        else:
            print(f"❌ API测试失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API测试异常: {str(e)}")
        return False

def test_webhook_api():
    """测试webhook API"""
    print("\n🔍 测试Webhook API...")
    
    webhook_data = {
        "object_kind": "push",
        "project": {
            "name": "test-project"
        },
        "commits": [
            {
                "message": "feat: 优化数据库连接池配置",
                "added": ["config/database.yaml"],
                "modified": ["terraform/rds.tf"],
                "removed": []
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/webhook/gitlab",
            json=webhook_data,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Webhook测试成功!")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return True
        else:
            print(f"❌ Webhook测试失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook测试异常: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== 简单API测试 ===")
    
    # 测试预测API
    predict_success = test_predict_api()
    
    # 测试webhook API
    webhook_success = test_webhook_api()
    
    print("\n📋 测试结果:")
    print(f"   预测API: {'✅ 成功' if predict_success else '❌ 失败'}")
    print(f"   Webhook API: {'✅ 成功' if webhook_success else '❌ 失败'}")
    
    if predict_success and webhook_success:
        print("\n🎉 所有API测试通过!")
    else:
        print("\n⚠️  部分API测试失败")