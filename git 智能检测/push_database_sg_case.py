#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库安全组变更测试用例推送脚本
将数据库安全组变更测试用例推送到GitLab仓库中
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
                print(f"✅ 分支创建成功: {branch_name}")
                return True
            elif response.status_code == 400 and 'already exists' in response.text:
                print(f"ℹ️  分支已存在: {branch_name}")
                return True
            else:
                print(f"❌ 分支创建失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 分支创建异常: {str(e)}")
            return False
    
    def create_file(self, file_path: str, content: str, branch: str, commit_message: str) -> bool:
        """创建文件"""
        url = f"{self.api_base}/repository/files/{file_path.replace('/', '%2F')}"
        
        # 将内容编码为base64
        content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        data = {
            'branch': branch,
            'content': content_b64,
            'commit_message': commit_message,
            'encoding': 'base64'
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, auth=self.auth, timeout=30)
            if response.status_code == 201:
                print(f"✅ 文件创建成功: {file_path}")
                return True
            else:
                print(f"❌ 文件创建失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 文件创建异常: {str(e)}")
            return False
    
    def create_merge_request(self, source_branch: str, target_branch: str, title: str, description: str) -> bool:
        """创建合并请求"""
        url = f"{self.api_base}/merge_requests"
        data = {
            'source_branch': source_branch,
            'target_branch': target_branch,
            'title': title,
            'description': description
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers, auth=self.auth, timeout=30)
            if response.status_code == 201:
                mr_data = response.json()
                print(f"✅ 合并请求创建成功: {mr_data.get('web_url')}")
                return True
            else:
                print(f"❌ 合并请求创建失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 合并请求创建异常: {str(e)}")
            return False
    
    def push_test_case(self, test_case: Dict[str, Any]) -> bool:
        """推送单个测试用例"""
        branch_name = test_case.get('branch', 'test/database-sg-change')
        
        # 1. 创建分支
        if not self.create_branch(branch_name):
            return False
        
        # 2. 创建测试用例信息文件
        test_info_content = json.dumps({
            'test_name': test_case.get('test_name'),
            'risk_level': test_case.get('risk_level'),
            'description': test_case.get('description'),
            'branch': branch_name,
            'author': test_case.get('author'),
            'commit_message': test_case.get('commit_message'),
            'timestamp': datetime.now().isoformat(),
            'files_changed': test_case.get('files_changed', []),
            'diff_content': test_case.get('diff_content', '')
        }, indent=2, ensure_ascii=False)
        
        if not self.create_file(
            'test_case_info.json',
            test_info_content,
            branch_name,
            f"add: {test_case.get('test_name')} - 测试用例信息"
        ):
            return False
        
        # 3. 创建配置文件
        for file_path in test_case.get('files_changed', []):
            if file_path.endswith('.json'):
                # 对于JSON文件，使用diff_content作为内容
                file_content = test_case.get('diff_content', '{}')
            else:
                # 对于其他文件，创建基本内容
                file_content = f"# {test_case.get('test_name')}\n# 配置文件\n"
            
            if not self.create_file(
                file_path,
                file_content,
                branch_name,
                f"add: {test_case.get('test_name')} - {file_path}"
            ):
                return False
        
        # 4. 创建差异文件
        diff_content = test_case.get('diff_content', '')
        if diff_content:
            if not self.create_file(
                'changes.diff',
                diff_content,
                branch_name,
                f"add: {test_case.get('test_name')} - 变更差异"
            ):
                return False
        
        # 5. 创建合并请求
        mr_title = f"🔒 {test_case.get('test_name')}"
        mr_description = f"""
# {test_case.get('test_name')}

## 测试用例描述

{test_case.get('description')}

## 风险等级

**{test_case.get('risk_level', 'unknown').upper()}**

## 变更信息

- **分支**: `{branch_name}`
- **作者**: {test_case.get('author')}
- **变更文件**: {', '.join(test_case.get('files_changed', []))}

## 变更内容

```json
{test_case.get('diff_content', '')}
```

---
*此合并请求由数据库安全组变更测试用例生成器自动创建*
        """
        
        if not self.create_merge_request(
            branch_name,
            'main',
            mr_title,
            mr_description
        ):
            return False
        
        return True

def generate_database_sg_test_case() -> Dict[str, Any]:
    """生成数据库安全组变更测试用例"""
    
    # 读取已创建的测试用例信息
    test_case_info_path = '/Users/heytea/Desktop/cursor/git 智能检测/gitlab_simulation/test/高风险---数据库安全组变更/test_case_info.json'
    
    try:
        with open(test_case_info_path, 'r', encoding='utf-8') as f:
            test_case_info = json.load(f)
        
        # 读取安全组配置文件
        sg_config_path = '/Users/heytea/Desktop/cursor/git 智能检测/gitlab_simulation/test/高风险---数据库安全组变更/security/database-sg-rules.json'
        with open(sg_config_path, 'r', encoding='utf-8') as f:
            sg_config = json.load(f)
        
        # 读取差异文件
        diff_path = '/Users/heytea/Desktop/cursor/git 智能检测/gitlab_simulation/test/高风险---数据库安全组变更/changes.diff'
        with open(diff_path, 'r', encoding='utf-8') as f:
            diff_content = f.read()
        
        return {
            'test_name': test_case_info['test_name'],
            'risk_level': test_case_info['risk_level'],
            'description': test_case_info['description'],
            'branch': test_case_info['branch'],
            'author': test_case_info['author'],
            'commit_message': test_case_info['commit_message'],
            'files_changed': test_case_info['files_changed'],
            'diff_content': json.dumps(sg_config, indent=2, ensure_ascii=False)
        }
    
    except Exception as e:
        print(f"❌ 读取测试用例文件失败: {str(e)}")
        # 返回默认测试用例
        return {
            'test_name': '高风险 - 数据库安全组变更',
            'risk_level': 'high',
            'description': '数据库安全组规则变更，涉及网络访问控制和数据安全',
            'branch': 'test/高风险---数据库安全组变更',
            'author': 'test-automation',
            'commit_message': 'test: 高风险 - 数据库安全组变更',
            'files_changed': ['security/database-sg-rules.json'],
            'diff_content': '''{
  "SecurityGroupId": "sg-database-prod-001",
  "GroupName": "database-production-sg",
  "Description": "Production database security group",
  "VpcId": "vpc-prod-main",
  "Rules": [
    {
      "Type": "Ingress",
      "IpProtocol": "TCP",
      "Port": "3306",
      "SourceSecurityGroupId": "sg-app-servers",
      "Description": "MySQL access from application servers"
    },
    {
      "Type": "Ingress",
      "IpProtocol": "TCP",
      "Port": "3306",
      "CidrIp": "10.0.0.0/8",
      "Description": "MySQL access from internal network"
    },
    {
      "Type": "Ingress",
      "IpProtocol": "TCP",
      "Port": "22",
      "CidrIp": "192.168.1.0/24",
      "Description": "SSH access from management subnet"
    },
    {
      "Type": "Egress",
      "IpProtocol": "ALL",
      "Port": "-1",
      "CidrIp": "0.0.0.0/0",
      "Description": "Allow all outbound traffic"
    }
  ],
  "Tags": [
    {
      "Key": "Environment",
      "Value": "Production"
    },
    {
      "Key": "Service",
      "Value": "Database"
    },
    {
      "Key": "CriticalLevel",
      "Value": "High"
    }
  ]
}'''
        }

def main():
    """主函数"""
    # GitLab配置
    GITLAB_URL = os.getenv('GITLAB_URL', 'http://10.251.0.16/gitlab-instance-1807000d')
    PROJECT_ID = os.getenv('GITLAB_PROJECT_ID', 'risk_detect')
    
    # 认证配置 - 优先使用用户名密码
    USERNAME = os.getenv('GITLAB_USERNAME')
    PASSWORD = os.getenv('GITLAB_PASSWORD')
    ACCESS_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN')
    
    # 检查环境变量
    if not GITLAB_URL or not PROJECT_ID:
        print("❌ 请设置以下环境变量:")
        print("   - GITLAB_URL: GitLab服务器地址")
        print("   - GITLAB_PROJECT_ID: 项目ID")
        return
    
    if not ((USERNAME and PASSWORD) or ACCESS_TOKEN):
        print("❌ 请设置认证信息:")
        print("   方式1 - 用户名密码认证:")
        print("     - GITLAB_USERNAME: GitLab用户名")
        print("     - GITLAB_PASSWORD: GitLab密码")
        print("   方式2 - 访问令牌认证:")
        print("     - GITLAB_ACCESS_TOKEN: 访问令牌")
        print("\n示例:")
        print("   export GITLAB_URL='http://10.251.0.16/gitlab-instance-1807000d'")
        print("   export GITLAB_PROJECT_ID='risk_detect'")
        print("   export GITLAB_USERNAME='root'")
        print("   export GITLAB_PASSWORD='your-password'")
        return
    
    try:
        # 生成数据库安全组变更测试用例
        print("📋 生成数据库安全组变更测试用例...")
        test_case = generate_database_sg_test_case()
        print(f"✅ 成功生成测试用例: {test_case['test_name']}")
        
        # 推送到GitLab
        if USERNAME and PASSWORD:
            print(f"🔐 使用用户名密码认证: {USERNAME}")
            pusher = GitLabPusher(GITLAB_URL, PROJECT_ID, username=USERNAME, password=PASSWORD)
        else:
            print(f"🔐 使用访问令牌认证")
            pusher = GitLabPusher(GITLAB_URL, PROJECT_ID, access_token=ACCESS_TOKEN)
        
        print(f"\n🚀 开始推送数据库安全组变更测试用例到GitLab...")
        
        if pusher.push_test_case(test_case):
            print(f"\n🎉 数据库安全组变更测试用例推送成功！")
            print(f"\n📊 推送详情:")
            print(f"   📝 测试用例: {test_case['test_name']}")
            print(f"   🔒 风险等级: {test_case['risk_level'].upper()}")
            print(f"   🌿 分支: {test_case['branch']}")
            print(f"   📁 变更文件: {', '.join(test_case['files_changed'])}")
        else:
            print(f"\n❌ 数据库安全组变更测试用例推送失败！")
            print(f"\n⚠️  请检查GitLab配置和网络连接")
    
    except Exception as e:
        print(f"❌ 执行过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()