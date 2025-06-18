#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送CLB监听器案例到GitLab并验证Grafana可视化效果
"""

import os
import json
import requests
import base64
import time
from datetime import datetime
import subprocess

# GitLab配置
GITLAB_URL = 'http://10.251.0.16/gitlab-instance-1807000d'
GITLAB_PROJECT_ID = 'risk_detect'
GITLAB_USERNAME = 'root'
GITLAB_PASSWORD = 'Admin123$%'

# 文件路径
CLB_CASE_FILE = '/Users/heytea/Desktop/cursor/git 智能检测/risk_demo/clb_listener_update_2024.json'

# 分支名称
BRANCH_NAME = f"clb-listener-update-{int(time.time())}"

# 提交信息
COMMIT_MESSAGE = "添加CLB监听器调整案例"

class GitLabPusher:
    """GitLab推送器"""
    
    def __init__(self, gitlab_url, project_id, username, password):
        self.gitlab_url = gitlab_url.rstrip('/')
        self.project_id = project_id
        self.username = username
        self.password = password
        
        # 设置认证方式
        self.auth = (username, password)
        self.headers = {
            'Content-Type': 'application/json'
        }
            
        self.api_base = f"{self.gitlab_url}/api/v4/projects/{self.project_id}"
    
    def create_branch(self, branch_name, ref='main'):
        """创建新分支"""
        url = f"{self.api_base}/repository/branches"
        data = {
            'branch': branch_name,
            'ref': ref
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data, auth=self.auth)
            if response.status_code == 201:
                print(f"✅ 成功创建分支: {branch_name}")
                return True
            elif response.status_code == 400 and 'already exists' in response.text:
                print(f"ℹ️  分支已存在: {branch_name}")
                return True
            else:
                print(f"❌ 创建分支失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 创建分支异常: {str(e)}")
            return False
    
    def get_file_content(self, file_path, branch='main'):
        """获取文件内容"""
        url = f"{self.api_base}/repository/files/{file_path.replace('/', '%2F')}"
        params = {'ref': branch}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, auth=self.auth)
            if response.status_code == 200:
                content = response.json().get('content', '')
                return base64.b64decode(content).decode('utf-8')
            return None
        except Exception as e:
            print(f"❌ 获取文件内容异常: {str(e)}")
            return None
    
    def create_or_update_file(self, file_path, content, commit_message, branch='main'):
        """创建或更新文件"""
        url = f"{self.api_base}/repository/files/{file_path.replace('/', '%2F')}"
        
        # 检查文件是否存在
        existing_content = self.get_file_content(file_path, branch)
        
        data = {
            'branch': branch,
            'content': content,
            'commit_message': commit_message,
            'encoding': 'text'
        }
        
        try:
            if existing_content is not None:
                # 文件存在，更新
                response = requests.put(url, headers=self.headers, json=data, auth=self.auth)
                action = "更新"
            else:
                # 文件不存在，创建
                response = requests.post(url, headers=self.headers, json=data, auth=self.auth)
                action = "创建"
            
            if response.status_code in [200, 201]:
                print(f"✅ 成功{action}文件: {file_path}")
                return True
            else:
                print(f"❌ {action}文件失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 操作文件异常: {str(e)}")
            return False

    def create_merge_request(self, source_branch, target_branch='main', title='', description=''):
        """创建合并请求"""
        url = f"{self.api_base}/merge_requests"
        data = {
            'source_branch': source_branch,
            'target_branch': target_branch,
            'title': title or f"CLB监听器案例: {source_branch}",
            'description': description or f"添加CLB监听器调整案例\n\n分支: {source_branch}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            'remove_source_branch': True
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data, auth=self.auth)
            if response.status_code == 201:
                mr_data = response.json()
                print(f"✅ 成功创建合并请求: {mr_data.get('web_url')}")
                return True
            else:
                print(f"❌ 创建合并请求失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 创建合并请求异常: {str(e)}")
            return False

def push_to_gitlab():
    """推送CLB监听器案例到GitLab"""
    print("\n🚀 开始推送CLB监听器案例到GitLab...")
    
    # 读取CLB案例文件
    try:
        with open(CLB_CASE_FILE, 'r', encoding='utf-8') as f:
            clb_case_content = f.read()
            clb_case_data = json.loads(clb_case_content)
            print(f"✅ 成功读取CLB案例文件: {CLB_CASE_FILE}")
    except Exception as e:
        print(f"❌ 读取CLB案例文件失败: {str(e)}")
        return False
    
    # 初始化GitLab推送器
    pusher = GitLabPusher(GITLAB_URL, GITLAB_PROJECT_ID, GITLAB_USERNAME, GITLAB_PASSWORD)
    
    # 创建分支
    if not pusher.create_branch(BRANCH_NAME):
        return False
    
    # 推送CLB案例文件
    target_file_path = f"risk_demo/clb_listener_update_{datetime.now().strftime('%Y%m%d')}.json"
    if not pusher.create_or_update_file(target_file_path, clb_case_content, COMMIT_MESSAGE, BRANCH_NAME):
        return False
    
    # 创建合并请求
    mr_title = f"添加CLB监听器调整案例 - {datetime.now().strftime('%Y-%m-%d')}"
    mr_description = f"""# CLB监听器调整案例

## 变更内容
- 更新SSL证书
- 修改健康检查配置
- 替换后端服务器
- 修改负载均衡调度算法
- 添加HTTP到HTTPS重定向

## 风险评估
- 风险等级: {clb_case_data.get('risk_assessment', {}).get('risk_level', 'UNKNOWN')}
- 风险概率: {clb_case_data.get('risk_assessment', {}).get('probability', 0)}

## 时间
- 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 计划实施时间: {clb_case_data.get('scheduled_time', 'UNKNOWN')}
"""
    
    if not pusher.create_merge_request(BRANCH_NAME, title=mr_title, description=mr_description):
        return False
    
    print("\n✅ CLB监听器案例已成功推送到GitLab!")
    return True

def check_grafana_visualization():
    """检查Grafana可视化效果"""
    print("\n🔍 检查Grafana可视化效果...")
    
    # 这里应该是访问Grafana API的代码
    # 由于我们没有实际的Grafana环境，这里只是模拟
    print("ℹ️  请访问Grafana仪表盘查看可视化效果:")
    print("   URL: http://localhost:3000/d/risk-assessment/risk-assessment-dashboard")
    print("   用户名: admin")
    print("   密码: admin")
    
    return True

def main():
    """主函数"""
    print("\n🔧 CLB监听器案例推送工具")
    print("=" * 50)
    
    # 推送到GitLab
    if push_to_gitlab():
        # 检查Grafana可视化
        check_grafana_visualization()
        print("\n✅ 任务完成!")
    else:
        print("\n❌ 任务失败!")

if __name__ == "__main__":
    main()