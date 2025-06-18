#!/usr/bin/env python3
import requests
import json

def test_webhook():
    # 读取测试数据
    with open('simple_test.json', 'r') as f:
        data = json.load(f)
    
    # 发送请求
    try:
        response = requests.post('http://localhost:8001/gitlab-webhook', json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Webhook测试成功!")
        else:
            print("❌ Webhook测试失败!")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    test_webhook()