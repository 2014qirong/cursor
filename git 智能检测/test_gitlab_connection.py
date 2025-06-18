#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitLab连接测试脚本
用于验证GitLab配置和权限
"""

import os
import requests
import json
from datetime import datetime

def test_gitlab_connection():
    """测试GitLab连接"""
    # GitLab配置
    GITLAB_URL = os.getenv('GITLAB_URL', 'http://10.251.0.16/gitlab-instance-1807000d')
    PROJECT_ID = os.getenv('GITLAB_PROJECT_ID', 'risk_detect')
    ACCESS_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN', 'your-access-token')
    
    print("🔍 GitLab连接测试")
    print("=" * 50)
    print(f"GitLab URL: {GITLAB_URL}")
    print(f"项目ID: {PROJECT_ID}")
    print(f"访问令牌: {ACCESS_TOKEN[:10]}..." if len(ACCESS_TOKEN) > 10 else "未设置")
    print()
    
    # 检查环境变量
    if ACCESS_TOKEN == 'your-access-token':
        print("❌ 请设置正确的GITLAB_ACCESS_TOKEN环境变量")
        print("   export GITLAB_ACCESS_TOKEN='your-real-token'")
        return False
    
    # 获取认证信息
    username = os.getenv('GITLAB_USERNAME')
    password = os.getenv('GITLAB_PASSWORD')
    
    if username and password:
        # 使用用户名密码认证
        auth = (username, password)
        headers = {'Content-Type': 'application/json'}
        print(f"🔐 使用用户名密码认证: {username}")
    else:
        # 使用访问令牌认证
        auth = None
        headers = {
            'PRIVATE-TOKEN': access_token,
            'Content-Type': 'application/json'
        }
        print(f"🔐 使用访问令牌认证")
    
    try:
        # 测试1: 验证用户身份
        print("1️⃣ 测试用户身份验证...")
        user_url = f"{GITLAB_URL}/api/v4/user"
        response = requests.get(user_url, headers=headers, auth=auth, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ 用户验证成功: {user_data.get('name', 'Unknown')} ({user_data.get('username', 'Unknown')})")
        else:
            print(f"   ❌ 用户验证失败: {response.status_code} - {response.text[:100]}")
            return False
        
        # 测试2: 获取项目信息
        print("\n2️⃣ 测试项目访问权限...")
        project_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}"
        response = requests.get(project_url, headers=headers, auth=auth, timeout=10)
        
        if response.status_code == 200:
            project_data = response.json()
            print(f"   ✅ 项目访问成功: {project_data.get('name', 'Unknown')}")
            print(f"   📁 项目路径: {project_data.get('path_with_namespace', 'Unknown')}")
            print(f"   🔒 访问级别: {project_data.get('visibility', 'Unknown')}")
        else:
            print(f"   ❌ 项目访问失败: {response.status_code} - {response.text[:100]}")
            return False
        
        # 测试3: 列出分支
        print("\n3️⃣ 测试分支访问...")
        branches_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/branches"
        response = requests.get(branches_url, headers=headers, auth=auth, timeout=10)
        
        if response.status_code == 200:
            branches = response.json()
            print(f"   ✅ 分支列表获取成功，共 {len(branches)} 个分支")
            for branch in branches[:3]:  # 显示前3个分支
                print(f"   📌 {branch.get('name', 'Unknown')}")
        else:
            print(f"   ❌ 分支访问失败: {response.status_code} - {response.text[:100]}")
            return False
        
        # 测试4: 创建测试分支
        print("\n4️⃣ 测试分支创建权限...")
        test_branch_name = f"test-connection-{int(datetime.now().timestamp())}"
        create_branch_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/branches"
        branch_data = {
            'branch': test_branch_name,
            'ref': 'main'  # 或者 'master'，取决于默认分支
        }
        
        response = requests.post(create_branch_url, headers=headers, json=branch_data, auth=auth, timeout=10)
        
        if response.status_code == 201:
            print(f"   ✅ 测试分支创建成功: {test_branch_name}")
            
            # 清理测试分支
            delete_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/repository/branches/{test_branch_name}"
            delete_response = requests.delete(delete_url, headers=headers, auth=auth, timeout=10)
            if delete_response.status_code == 204:
                print(f"   🧹 测试分支已清理")
        else:
            print(f"   ❌ 分支创建失败: {response.status_code} - {response.text[:100]}")
            if response.status_code == 403:
                print("   💡 提示: 可能缺少Developer权限")
            return False
        
        print("\n🎉 所有测试通过！GitLab配置正确，可以进行推送操作。")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络连接错误: {str(e)}")
        print("💡 请检查:")
        print("   - 网络连接是否正常")
        print("   - GitLab服务器地址是否正确")
        print("   - 防火墙设置")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        return False

def main():
    """主函数"""
    print("GitLab连接测试工具")
    print("=" * 50)
    print("使用方法:")
    print("方式1 - 用户名密码认证:")
    print("  export GITLAB_USERNAME='root'")
    print("  export GITLAB_PASSWORD='your-password'")
    print("方式2 - 访问令牌认证:")
    print("  export GITLAB_ACCESS_TOKEN='your-token'")
    print("然后运行: python3 test_gitlab_connection.py")
    print("=" * 50)
    print()
    
    success = test_gitlab_connection()
    
    if success:
        print("\n✅ 连接测试成功！现在可以运行 push_to_gitlab.py 进行推送。")
    else:
        print("\n❌ 连接测试失败，请检查配置后重试。")
        print("\n📋 故障排除步骤:")
        print("1. 确认GitLab访问令牌有效且具有api权限")
        print("2. 确认用户对项目有Developer或更高权限")
        print("3. 确认网络连接正常")
        print("4. 查看详细错误信息进行诊断")

if __name__ == "__main__":
    main()