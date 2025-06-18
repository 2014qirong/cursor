#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_gitlab_api():
    """测试GitLab API连接"""
    base_url = 'http://10.251.0.16/gitlab-instance-1807000d'
    auth = ('root', 'Admin123$%')
    
    # 测试基本连接
    print("1. 测试基本连接...")
    try:
        response = requests.get(base_url, auth=auth, timeout=10)
        print(f"基本连接状态码: {response.status_code}")
    except Exception as e:
        print(f"基本连接失败: {e}")
        return
    
    # 测试API端点
    print("\n2. 测试API端点...")
    api_url = f'{base_url}/api/v4/projects'
    try:
        response = requests.get(api_url, auth=auth, timeout=10)
        print(f"API状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"响应内容前200字符: {response.text[:200]}")
            if response.text.strip():
                try:
                    projects = response.json()
                    print(f"找到 {len(projects)} 个项目:")
                    for project in projects:
                        print(f"  ID: {project['id']}, 名称: {project['name']}, 路径: {project['path']}")
                        if project['name'] == 'risk_detect' or project['path'] == 'risk_detect':
                            print(f"  ✅ 找到目标项目! ID: {project['id']}")
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误: {e}")
                    print(f"原始响应: {response.text}")
            else:
                print("响应为空")
        elif response.status_code == 401:
            print("认证失败，请检查用户名密码")
        elif response.status_code == 403:
            print("权限不足，请检查用户权限")
        else:
            print(f"错误响应: {response.text[:500]}")
            
    except Exception as e:
        print(f"API连接错误: {e}")

if __name__ == '__main__':
    test_gitlab_api()