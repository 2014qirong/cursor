#!/usr/bin/env python3
import requests
import json

# 读取测试payload
with open('test_webhook_payload.json', 'r') as f:
    data = json.load(f)

# 发送POST请求到webhook端点
try:
    response = requests.post(
        'http://localhost:8001/gitlab-webhook',
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print(f'Status Code: {response.status_code}')
    print(f'Response Headers: {dict(response.headers)}')
    print(f'Response Body: {response.text}')
except Exception as e:
    print(f'Error: {e}')