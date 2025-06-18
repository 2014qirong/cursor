#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云原生API网关测试用例推送脚本
将生成的测试用例推送到GitLab仓库中
"""

import os
import json
import requests
import base64
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from test_tencent_api_gateway import api_gateway_test_cases, _generate_plugin_config_change, _generate_high_risk_production_change, _generate_database_config_change, _generate_secret_management_change

class GitLabPusher:
    """GitLab推送器"""
    
    def __init__(self, gitlab_url: str, project_id: str, username: str = None, password: str = None, access_token: str = None):
        self.gitlab_url = gitlab_url.rstrip('/')
        self.project_id = project_id
        self.username = username
        self.password = password
        self.access_token = access_token
        
        # 读取自动推送规则配置
        self.auto_push_to_main = os.getenv('GITLAB_AUTO_PUSH_TO_MAIN', 'false').lower() == 'true'
        self.skip_confirmation = os.getenv('GITLAB_SKIP_CONFIRMATION', 'false').lower() == 'true'
        self.default_branch = os.getenv('GITLAB_DEFAULT_BRANCH', 'main')
        
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
    
    def get_file_content(self, file_path: str, branch: str = 'main') -> Optional[str]:
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
    
    def create_or_update_file(self, file_path: str, content: str, 
                             commit_message: str, branch: str = 'main') -> bool:
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
            print(f"❌ {action}文件异常: {str(e)}")
            return False
    
    def create_merge_request(self, source_branch: str, target_branch: str = 'main',
                           title: str = '', description: str = '') -> bool:
        """创建合并请求"""
        url = f"{self.api_base}/merge_requests"
        data = {
            'source_branch': source_branch,
            'target_branch': target_branch,
            'title': title or f"API网关测试用例: {source_branch}",
            'description': description or f"自动生成的腾讯云API网关测试用例\n\n分支: {source_branch}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
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
    
    def push_test_case(self, test_case: Dict[str, Any]) -> bool:
        """推送单个测试用例"""
        # 检查是否启用自动推送到主干
        if self.auto_push_to_main:
            return self.push_directly_to_main(test_case)
        
        branch_name = test_case.get('branch', f"test-case-{int(time.time())}")
        
        # 创建分支
        if not self.create_branch(branch_name):
            return False
        
        # 推送文件变更
        success = True
        for file_path in test_case.get('files_changed', []):
            # 读取本地文件内容
            local_file_path = os.path.join('/Users/heytea/Desktop/cursor/git 智能检测', file_path)
            
            if os.path.exists(local_file_path):
                with open(local_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 应用diff变更（简化处理，实际应该解析diff）
                if test_case.get('diff_content'):
                    # 这里简化处理，实际项目中应该正确解析和应用diff
                    content += f"\n\n# 测试变更 - {test_case.get('test_name')}\n"
                    content += f"# 风险等级: {test_case.get('risk_level')}\n"
                    content += f"# 描述: {test_case.get('description')}\n"
                
                if not self.create_or_update_file(
                    file_path, content, 
                    test_case.get('commit_message', f"测试用例: {test_case.get('test_name')}"),
                    branch_name
                ):
                    success = False
            else:
                # 创建新文件
                content = f"# {test_case.get('test_name')}\n"
                content += f"# 风险等级: {test_case.get('risk_level')}\n"
                content += f"# 描述: {test_case.get('description')}\n\n"
                content += test_case.get('diff_content', '')
                
                if not self.create_or_update_file(
                    file_path, content,
                    test_case.get('commit_message', f"测试用例: {test_case.get('test_name')}"),
                    branch_name
                ):
                    success = False
        
        # 创建合并请求
        if success:
            self.create_merge_request(
                branch_name,
                title=f"[测试用例] {test_case.get('test_name')}",
                description=f"""
## 测试用例信息

- **名称**: {test_case.get('test_name')}
- **风险等级**: {test_case.get('risk_level')}
- **描述**: {test_case.get('description')}
- **作者**: {test_case.get('author')}
- **变更文件**: {', '.join(test_case.get('files_changed', []))}

## 变更内容

```diff
{test_case.get('diff_content', '')}
```

---
*此合并请求由腾讯云API网关测试用例生成器自动创建*
                """
            )
        
        return success
    
    def push_directly_to_main(self, test_case: Dict[str, Any]) -> bool:
        """直接推送到主干分支，无需创建分支和合并请求"""
        print(f"🚀 启用自动推送模式，直接推送到 {self.default_branch} 分支")
        
        success = True
        for file_path in test_case.get('files_changed', []):
            # 读取本地文件内容
            local_file_path = os.path.join('/Users/heytea/Desktop/cursor/git 智能检测', file_path)
            
            if os.path.exists(local_file_path):
                with open(local_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 应用diff变更
                if test_case.get('diff_content'):
                    content += f"\n\n# 测试变更 - {test_case.get('test_name')}\n"
                    content += f"# 风险等级: {test_case.get('risk_level')}\n"
                    content += f"# 描述: {test_case.get('description')}\n"
                
                if not self.create_or_update_file(
                    file_path, content, 
                    test_case.get('commit_message', f"自动推送: {test_case.get('test_name')}"),
                    self.default_branch
                ):
                    success = False
            else:
                # 创建新文件
                content = f"# {test_case.get('test_name')}\n"
                content += f"# 风险等级: {test_case.get('risk_level')}\n"
                content += f"# 描述: {test_case.get('description')}\n\n"
                content += test_case.get('diff_content', '')
                
                if not self.create_or_update_file(
                    file_path, content,
                    test_case.get('commit_message', f"自动推送: {test_case.get('test_name')}"),
                    self.default_branch
                ):
                    success = False
        
        if success:
            print(f"✅ 成功直接推送到 {self.default_branch} 分支")
        else:
            print(f"❌ 推送到 {self.default_branch} 分支失败")
        
        return success
    
    def push_all_test_cases(self, test_cases: List[Dict[str, Any]]) -> Dict[str, int]:
        """推送所有测试用例"""
        results = {'success': 0, 'failed': 0}
        
        print(f"🚀 开始推送 {len(test_cases)} 个测试用例到GitLab...")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 [{i}/{len(test_cases)}] 推送测试用例: {test_case.get('test_name')}")
            
            if self.push_test_case(test_case):
                results['success'] += 1
                print(f"✅ 测试用例推送成功")
            else:
                results['failed'] += 1
                print(f"❌ 测试用例推送失败")
            
            # 避免API限流
            time.sleep(2)
        
        return results

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
        # 生成测试用例
        print("📋 生成腾讯云API网关测试用例...")
        test_cases = []
        
        # 添加基础测试用例
        for case in api_gateway_test_cases:
            test_cases.append({
                'test_name': case['name'],
                'risk_level': 'high',
                'description': case['name'],
                'files_changed': ['config/api-gateway-config.yaml'],
                'diff_content': json.dumps(case['data'], indent=2),
                'commit_message': f"test: {case['name']}",
                'author': 'test-automation',
                'branch': f"test/{case['name'].lower().replace(' ', '-').replace('-', '_')}"
            })
        
        # 添加额外的测试用例
        test_cases.extend([
            _generate_plugin_config_change(),
            _generate_high_risk_production_change(),
            _generate_database_config_change(),
            _generate_secret_management_change()
        ])
        
        print(f"✅ 成功生成 {len(test_cases)} 个测试用例")
        
        # 推送到GitLab
        if USERNAME and PASSWORD:
            print(f"🔐 使用用户名密码认证: {USERNAME}")
            pusher = GitLabPusher(GITLAB_URL, PROJECT_ID, username=USERNAME, password=PASSWORD)
        else:
            print(f"🔐 使用访问令牌认证")
            pusher = GitLabPusher(GITLAB_URL, PROJECT_ID, access_token=ACCESS_TOKEN)
        
        results = pusher.push_all_test_cases(test_cases)
        
        # 输出结果
        print(f"\n📊 推送结果统计:")
        print(f"   ✅ 成功: {results['success']} 个")
        print(f"   ❌ 失败: {results['failed']} 个")
        print(f"   📈 成功率: {results['success']/(results['success']+results['failed'])*100:.1f}%")
        
        if results['failed'] > 0:
            print(f"\n⚠️  有 {results['failed']} 个测试用例推送失败，请检查GitLab配置和网络连接")
        else:
            print(f"\n🎉 所有测试用例推送成功！")
    
    except Exception as e:
        print(f"❌ 执行过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()