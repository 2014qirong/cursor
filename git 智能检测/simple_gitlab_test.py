#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os

def test_simple_connection():
    """简单的GitLab连接测试"""
    
    # 配置
    GITLAB_URL = "http://10.251.0.16/gitlab-instance-1807000d"
    USERNAME = "root"
    PASSWORD = "Admin123$%"
    
    # 使用用户名密码认证
    auth = (USERNAME, PASSWORD)
    headers = {
        'Content-Type': 'application/json'
    }
    
    print(f"测试GitLab连接: {GITLAB_URL}")
    print(f"使用用户名: {USERNAME}")
    print()
    
    try:
        # 测试用户API
        user_url = f"{GITLAB_URL}/api/v4/user"
        print(f"请求URL: {user_url}")
        
        response = requests.get(user_url, headers=headers, auth=auth, timeout=10)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text[:500]}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"\n✅ 连接成功!")
            print(f"用户: {user_data.get('name', 'Unknown')}")
            print(f"用户名: {user_data.get('username', 'Unknown')}")
            return True
        else:
            print(f"\n❌ 连接失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ 连接错误: {str(e)}")
        return False

if __name__ == "__main__":
    test_simple_connection()