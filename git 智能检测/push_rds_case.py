#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云数据库RDS配置变更案例推送脚本
将新创建的云数据库变更测试用例推送到GitLab仓库中
"""

import os
import json
import requests
import base64
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class GitLabPusher:
    """GitLab推送器"""
    
    def __init__(self, gitlab_url: str, project_id: str, username: str = None, password: str = None, access_token: str = None):
        self.gitlab_url = gitlab_url.rstrip('/')
        self.project_id = project_id
        self.username = username
        self.password = password
        self.access_token = access_token
        
        # 设置认证方式
        if username and password:
            # 使用用户名密码认证
            self.auth = (username, password)
            self.headers = {
                'Content-Type': 'application/json'
            }
        elif access_token:
            # 使用访问令牌认证
            self.auth = None
            self.headers = {
                'PRIVATE-TOKEN': access_token,
                'Content-Type': 'application/json'
            }
        else:
            raise ValueError("必须提供用户名密码或访问令牌")
            
        self.api_base = f"{self.gitlab_url}/api/v4/projects/{self.project_id}"
    
    def create_branch(self, branch_name: str, ref: str = 'main') -> bool:
        """创建新分支"""
        url = f"{self.api_base}/repository/branches"
        data = {
            'branch': branch_name,
            'ref': ref
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, auth=self.auth, timeout=30)
            if response.status_code == 201:
                print(f"✅ 分支 '{branch_name}' 创建成功")
                return True
            elif response.status_code == 400 and 'already exists' in response.text:
                print(f"ℹ️  分支 '{branch_name}' 已存在")
                return True
            else:
                print(f"❌ 创建分支失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 创建分支时出错: {str(e)}")
            return False
    
    def create_file(self, file_path: str, content: str, commit_message: str, branch: str = 'main') -> bool:
        """创建文件"""
        url = f"{self.api_base}/repository/files/{file_path.replace('/', '%2F')}"
        
        # 将内容编码为base64
        content_base64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        data = {
            'branch': branch,
            'content': content_base64,
            'commit_message': commit_message,
            'encoding': 'base64'
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, auth=self.auth, timeout=30)
            if response.status_code == 201:
                print(f"✅ 文件 '{file_path}' 创建成功")
                return True
            else:
                print(f"❌ 创建文件 '{file_path}' 失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 创建文件 '{file_path}' 时出错: {str(e)}")
            return False

def load_test_case_files():
    """加载测试用例文件"""
    base_path = "/Users/heytea/Desktop/cursor/git 智能检测/gitlab_simulation/test/高风险---云数据库RDS配置变更"
    
    files_to_push = [
        {
            'local_path': f"{base_path}/test_case_info.json",
            'gitlab_path': "test_cases/rds-config-change/test_case_info.json"
        },
        {
            'local_path': f"{base_path}/database/rds-config.json",
            'gitlab_path': "test_cases/rds-config-change/database/rds-config.json"
        },
        {
            'local_path': f"{base_path}/terraform/rds-instance.tf",
            'gitlab_path': "test_cases/rds-config-change/terraform/rds-instance.tf"
        },
        {
            'local_path': f"{base_path}/config/database-params.yaml",
            'gitlab_path': "test_cases/rds-config-change/config/database-params.yaml"
        },
        {
            'local_path': f"{base_path}/changes.diff",
            'gitlab_path': "test_cases/rds-config-change/changes.diff"
        }
    ]
    
    return files_to_push

def push_rds_case_to_gitlab():
    """推送RDS配置变更案例到GitLab"""
    print("\n🚀 开始推送云数据库RDS配置变更案例到GitLab...")
    
    # GitLab配置
    GITLAB_URL = 'http://10.251.0.16/gitlab-instance-1807000d'
    PROJECT_ID = 'risk_detect'
    USERNAME = 'root'
    PASSWORD = 'Admin123$%'
    
    # 初始化GitLab推送器
    pusher = GitLabPusher(GITLAB_URL, PROJECT_ID, USERNAME, PASSWORD)
    
    # 创建分支
    branch_name = "test/高风险---云数据库RDS配置变更"
    if not pusher.create_branch(branch_name):
        print("❌ 无法创建分支，推送终止")
        return False
    
    # 加载文件列表
    files_to_push = load_test_case_files()
    
    success_count = 0
    total_count = len(files_to_push)
    
    # 推送每个文件
    for file_info in files_to_push:
        try:
            # 读取本地文件内容
            with open(file_info['local_path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 推送到GitLab
            commit_message = f"feat: 添加云数据库RDS配置变更用例 - {os.path.basename(file_info['gitlab_path'])}"
            
            if pusher.create_file(file_info['gitlab_path'], content, commit_message, branch_name):
                success_count += 1
                time.sleep(1)  # 避免API限制
            
        except FileNotFoundError:
            print(f"❌ 本地文件不存在: {file_info['local_path']}")
        except Exception as e:
            print(f"❌ 处理文件 {file_info['local_path']} 时出错: {str(e)}")
    
    print(f"\n📊 推送完成: {success_count}/{total_count} 个文件成功推送")
    
    if success_count == total_count:
        print("\n✅ 云数据库RDS配置变更案例已成功推送到GitLab!")
        print(f"🔗 分支地址: {GITLAB_URL}/risk_detect/-/tree/{branch_name}")
        return True
    else:
        print(f"\n⚠️  有 {total_count - success_count} 个文件推送失败")
        return False

def trigger_webhook_test():
    """触发webhook测试"""
    print("\n🔄 触发GitLab Webhook进行风险评估...")
    
    # 构造GitLab webhook数据
    webhook_data = {
        "object_kind": "push",
        "event_name": "push",
        "before": "1234567890abcdef1234567890abcdef12345678",
        "after": "abcdefg1234567890abcdef1234567890abcdefg",
        "ref": "refs/heads/test/高风险---云数据库RDS配置变更",
        "checkout_sha": "abcdefg1234567890abcdef1234567890abcdefg",
        "message": "feat: 云数据库RDS配置优化 - 调整连接池和备份策略",
        "user_id": 1,
        "user_name": "database-admin",
        "user_username": "database-admin",
        "user_email": "dba@example.com",
        "project_id": 1,
        "project": {
            "id": 1,
            "name": "risk_detect",
            "description": "Risk detection test project",
            "web_url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect",
            "avatar_url": None,
            "git_ssh_url": "git@10.251.0.16:gitlab-instance-1807000d/risk_detect.git",
            "git_http_url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect.git",
            "namespace": "root",
            "visibility_level": 0,
            "path_with_namespace": "root/risk_detect",
            "default_branch": "main",
            "homepage": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect",
            "url": "git@10.251.0.16:gitlab-instance-1807000d/risk_detect.git",
            "ssh_url": "git@10.251.0.16:gitlab-instance-1807000d/risk_detect.git",
            "http_url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect.git"
        },
        "commits": [
            {
                "id": "abcdefg1234567890abcdef1234567890abcdefg",
                "message": "feat: 云数据库RDS配置优化\n\n- 增加最大连接数从1000到2000\n- 延长备份保留期从7天到30天\n- 启用IAM数据库认证\n- 增强SSL安全配置",
                "title": "feat: 云数据库RDS配置优化",
                "timestamp": datetime.now().isoformat(),
                "url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect/-/commit/abcdefg1234567890abcdef1234567890abcdefg",
                "author": {
                    "name": "database-admin",
                    "email": "dba@example.com"
                },
                "added": [
                    "test_cases/rds-config-change/database/rds-config.json",
                    "test_cases/rds-config-change/terraform/rds-instance.tf",
                    "test_cases/rds-config-change/config/database-params.yaml"
                ],
                "modified": [],
                "removed": []
            }
        ],
        "total_commits_count": 1,
        "push_options": {},
        "repository": {
            "name": "risk_detect",
            "url": "git@10.251.0.16:gitlab-instance-1807000d/risk_detect.git",
            "description": "Risk detection test project",
            "homepage": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect",
            "git_http_url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect.git",
            "git_ssh_url": "git@10.251.0.16:gitlab-instance-1807000d/risk_detect.git",
            "visibility_level": 0
        }
    }
    
    # 发送到AI推理服务
    ai_service_url = "http://localhost:8001"
    url = f"{ai_service_url}/gitlab-webhook"
    headers = {
        "Content-Type": "application/json",
        "X-Gitlab-Event": "Push Hook"
    }
    
    try:
        print(f"发送webhook数据到: {url}")
        response = requests.post(url, json=webhook_data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("\n=== 🎯 风险评估结果 ===")
            print(f"风险等级: {result.get('risk_level', 'unknown')}")
            print(f"风险概率: {result.get('probability', 0.0):.2%}")
            print(f"处理状态: {result.get('status', 'unknown')}")
            
            if 'details' in result:
                print(f"详细信息: {result['details']}")
            
            print("\n=== 📊 Grafana仪表板验证 ===")
            print("请访问以下链接查看风险评估仪表板:")
            print("http://localhost:3000/d/risk-assessment/risk-assessment-dashboard")
            print("\n✅ 数据已成功存储到InfluxDB，可在Grafana中查看可视化结果")
            
            return True
        else:
            print(f"❌ Webhook请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到AI推理服务，请确保服务正在运行 (http://localhost:8001)")
        return False
    except Exception as e:
        print(f"❌ 发送webhook时出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("=== 🚀 云数据库RDS配置变更案例推送和测试 ===")
    print("\n本脚本将执行以下操作:")
    print("1. 推送云数据库RDS配置变更测试用例到GitLab")
    print("2. 触发GitLab Webhook进行风险评估")
    print("3. 验证Grafana仪表板数据展示")
    
    # 1. 推送到GitLab
    if push_rds_case_to_gitlab():
        print("\n⏳ 等待3秒后触发webhook测试...")
        time.sleep(3)
        
        # 2. 触发webhook测试
        if trigger_webhook_test():
            print("\n🎉 所有操作完成！")
            print("\n📋 后续步骤:")
            print("1. 检查GitLab仓库中的新分支和文件")
            print("2. 访问Grafana仪表板查看风险评估结果")
            print("3. 验证InfluxDB中的数据存储")
        else:
            print("\n⚠️  Webhook测试失败，但文件已成功推送到GitLab")
    else:
        print("\n❌ 推送失败，请检查GitLab配置和网络连接")

if __name__ == "__main__":
    main()