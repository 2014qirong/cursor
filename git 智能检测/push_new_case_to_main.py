#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送新的数据库连接池配置变更用例到GitLab主干
"""

import os
import json
import requests
import time
from datetime import datetime

# GitLab配置
GITLAB_URL = "http://localhost:8080"  # 本地GitLab实例
PROJECT_ID = "1"  # 项目ID
USERNAME = "root"  # GitLab用户名
PASSWORD = "password123"  # GitLab密码
ACCESS_TOKEN = "glpat-xxxxxxxxxxxxxxxxxxxx"  # 如果有访问令牌

class GitLabPusher:
    """GitLab推送器"""
    
    def __init__(self, gitlab_url: str, project_id: str, username: str = None, password: str = None):
        self.gitlab_url = gitlab_url.rstrip('/')
        self.project_id = project_id
        self.username = username
        self.password = password
        
        # 使用用户名密码认证
        self.auth = (username, password) if username and password else None
        self.headers = {
            'Content-Type': 'application/json'
        }
            
        self.api_base = f"{self.gitlab_url}/api/v4/projects/{self.project_id}"
    
    def create_file(self, file_path: str, content: str, commit_message: str, branch: str = 'main') -> bool:
        """在指定分支创建文件"""
        url = f"{self.api_base}/repository/files/{file_path.replace('/', '%2F')}"
        
        data = {
            'branch': branch,
            'content': content,
            'commit_message': commit_message,
            'encoding': 'text'
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, auth=self.auth, timeout=30)
            if response.status_code == 201:
                print(f"✅ 成功创建文件: {file_path}")
                return True
            else:
                print(f"❌ 创建文件失败: {file_path}, 状态码: {response.status_code}")
                print(f"   响应: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 创建文件异常: {file_path}, 错误: {str(e)}")
            return False
    
    def push_database_config_case(self) -> bool:
        """推送数据库连接池配置变更用例"""
        print("🚀 开始推送数据库连接池配置变更用例到主干...")
        
        # 读取本地文件内容
        base_path = "/Users/heytea/Desktop/cursor/git 智能检测/gitlab_simulation/feature/database-connection-pool-update"
        
        files_to_push = [
            {
                'local_path': f"{base_path}/test_case_info.json",
                'gitlab_path': "test_cases/database-connection-pool-update/test_case_info.json"
            },
            {
                'local_path': f"{base_path}/changes.diff",
                'gitlab_path': "test_cases/database-connection-pool-update/changes.diff"
            },
            {
                'local_path': f"{base_path}/config/database-config.yaml",
                'gitlab_path': "test_cases/database-connection-pool-update/config/database-config.yaml"
            },
            {
                'local_path': f"{base_path}/terraform/rds-config.tf",
                'gitlab_path': "test_cases/database-connection-pool-update/terraform/rds-config.tf"
            }
        ]
        
        success_count = 0
        total_count = len(files_to_push)
        
        for file_info in files_to_push:
            try:
                # 读取本地文件内容
                with open(file_info['local_path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 推送到GitLab主干
                commit_message = f"feat: 添加数据库连接池配置变更用例 - {os.path.basename(file_info['gitlab_path'])}"
                
                if self.create_file(file_info['gitlab_path'], content, commit_message, 'main'):
                    success_count += 1
                    time.sleep(1)  # 避免请求过快
                
            except FileNotFoundError:
                print(f"❌ 本地文件不存在: {file_info['local_path']}")
            except Exception as e:
                print(f"❌ 处理文件时出错: {file_info['local_path']}, 错误: {str(e)}")
        
        print(f"\n📊 推送结果: {success_count}/{total_count} 个文件成功推送到主干")
        return success_count == total_count

def trigger_webhook_test():
    """触发webhook测试，验证风险评估"""
    print("\n🔔 触发webhook测试...")
    
    # 模拟GitLab webhook数据
    webhook_data = {
        "object_kind": "push",
        "event_name": "push",
        "before": "0000000000000000000000000000000000000000",
        "after": "db_pool_001",
        "ref": "refs/heads/main",
        "project_id": 301,
        "project": {
            "id": 301,
            "name": "database-infrastructure",
            "namespace": "backend",
            "web_url": "http://localhost:8080/backend/database-infrastructure"
        },
        "commits": [
            {
                "id": "db_pool_001",
                "message": "feat: 优化数据库连接池配置以提升性能",
                "timestamp": datetime.now().isoformat(),
                "url": "http://localhost:8080/backend/database-infrastructure/-/commit/db_pool_001",
                "author": {
                    "name": "Database Team",
                    "email": "database-team@company.com"
                },
                "added": [
                    "monitoring/db-pool-metrics.yaml"
                ],
                "modified": [
                    "config/database-config.yaml",
                    "terraform/rds-config.tf",
                    "helm/database-values.yaml"
                ],
                "removed": []
            }
        ]
    }
    
    try:
        # 发送到本地风险评估API
        response = requests.post(
            "http://localhost:8001/webhook/gitlab",
            json=webhook_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Webhook测试成功!")
            print(f"📊 风险评估结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return True
        else:
            print(f"❌ Webhook测试失败: HTTP {response.status_code}")
            print(f"   响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook测试异常: {str(e)}")
        return False

def check_grafana_data():
    """检查Grafana中的数据"""
    print("\n📈 检查Grafana数据...")
    
    try:
        # 等待数据写入InfluxDB
        print("⏳ 等待数据写入InfluxDB (10秒)...")
        time.sleep(10)
        
        # 检查Grafana健康状态
        response = requests.get(
            "http://localhost:3000/api/health",
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Grafana服务正常运行")
            print("🔗 请访问 http://localhost:3000 查看风险评估仪表板")
            print("   用户名: admin")
            print("   密码: admin123")
            return True
        else:
            print(f"❌ Grafana服务异常: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 检查Grafana时出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("=== 数据库连接池配置变更用例推送测试 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 1. 推送变更用例到GitLab主干
        pusher = GitLabPusher(GITLAB_URL, PROJECT_ID, USERNAME, PASSWORD)
        push_success = pusher.push_database_config_case()
        
        if not push_success:
            print("❌ 推送失败，跳过后续测试")
            return
        
        # 2. 触发webhook测试
        webhook_success = trigger_webhook_test()
        
        if not webhook_success:
            print("❌ Webhook测试失败")
            return
        
        # 3. 检查Grafana数据
        grafana_success = check_grafana_data()
        
        if grafana_success:
            print("\n🎉 完整测试流程成功完成!")
            print("📋 测试总结:")
            print("   ✅ 变更用例已推送到GitLab主干")
            print("   ✅ 风险评估API正常响应")
            print("   ✅ Grafana仪表板可以查看")
        else:
            print("\n⚠️  测试部分完成，请手动检查Grafana")
            
    except Exception as e:
        print(f"❌ 执行过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()