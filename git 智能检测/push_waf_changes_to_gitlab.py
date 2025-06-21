#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitLab推送脚本 - WAF高风险变更
功能：将WAF配置变更推送到GitLab仓库main分支
触发：AI风险评估webhook
"""

import os
import json
import time
import subprocess
import requests
from datetime import datetime
from typing import Dict, Any, List

class GitLabPusher:
    """
    GitLab推送管理类
    """
    
    def __init__(self):
        self.repo_path = os.getcwd()
        self.gitlab_token = os.getenv('GITLAB_TOKEN', '${GITLAB_TOKEN}')
        self.gitlab_url = os.getenv('GITLAB_URL', 'https://gitlab.example.com')
        self.project_id = os.getenv('GITLAB_PROJECT_ID', '${PROJECT_ID}')
        self.webhook_url = 'http://localhost:8001/gitlab-webhook'
        
        # 变更文件列表
        self.change_files = [
            'waf_security_policy_change.yaml',
            'tencent_waf_api_operations.py'
        ]
        
        self.push_results = []
        
    def check_git_status(self) -> Dict[str, Any]:
        """
        检查Git仓库状态
        """
        try:
            # 检查是否在Git仓库中
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': 'Not in a git repository or git not available',
                    'details': result.stderr
                }
            
            # 获取当前分支
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True, cwd=self.repo_path)
            current_branch = branch_result.stdout.strip()
            
            # 获取未提交的文件
            modified_files = []
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        status = line[:2]
                        filename = line[3:]
                        modified_files.append({
                            'status': status,
                            'filename': filename
                        })
            
            return {
                'success': True,
                'current_branch': current_branch,
                'modified_files': modified_files,
                'is_clean': len(modified_files) == 0
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def switch_to_main_branch(self) -> Dict[str, Any]:
        """
        切换到main分支
        """
        try:
            print("🔄 切换到main分支...")
            
            # 检查main分支是否存在
            branch_check = subprocess.run(['git', 'branch', '-a'], 
                                        capture_output=True, text=True, cwd=self.repo_path)
            
            if 'main' not in branch_check.stdout and 'origin/main' not in branch_check.stdout:
                # 如果main分支不存在，创建它
                result = subprocess.run(['git', 'checkout', '-b', 'main'], 
                                      capture_output=True, text=True, cwd=self.repo_path)
            else:
                # 切换到main分支
                result = subprocess.run(['git', 'checkout', 'main'], 
                                      capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode == 0:
                print("✅ 成功切换到main分支")
                return {
                    'success': True,
                    'message': 'Successfully switched to main branch',
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'output': result.stdout
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_and_commit_changes(self) -> Dict[str, Any]:
        """
        添加并提交变更文件
        """
        try:
            print("📝 添加变更文件到Git...")
            
            # 添加所有变更文件
            for file_path in self.change_files:
                if os.path.exists(file_path):
                    add_result = subprocess.run(['git', 'add', file_path], 
                                              capture_output=True, text=True, cwd=self.repo_path)
                    if add_result.returncode != 0:
                        print(f"⚠️  添加文件 {file_path} 失败: {add_result.stderr}")
                    else:
                        print(f"✅ 已添加文件: {file_path}")
                else:
                    print(f"⚠️  文件不存在: {file_path}")
            
            # 创建提交信息
            commit_message = f"""🚨 CRITICAL: 生产环境WAF安全策略紧急变更

变更类型: 高风险WAF配置调整
风险等级: CRITICAL
变更时间: {datetime.now().isoformat()}
有效期: 1-2小时

变更内容:
- 创建全网IP白名单规则 (0.0.0.0/0)
- 防护模式从拦截改为观察模式
- 禁用SQL注入和XSS检测规则
- 关闭CC防护和Bot防护
- 修改IP访问控制规则
- 调整负载均衡器配置

⚠️ 警告: 此变更将显著降低WAF安全防护能力
🔄 回滚方案: 已准备，预计5-10分钟完成
👥 审批人: security-team@company.com
📋 变更单号: CR-2024-0115-001

影响文件:
- waf_security_policy_change.yaml
- tencent_waf_api_operations.py

#emergency #critical #waf #security #production"""
            
            # 提交变更
            commit_result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                         capture_output=True, text=True, cwd=self.repo_path)
            
            if commit_result.returncode == 0:
                print("✅ 变更已成功提交")
                
                # 获取提交哈希
                hash_result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                           capture_output=True, text=True, cwd=self.repo_path)
                commit_hash = hash_result.stdout.strip() if hash_result.returncode == 0 else 'unknown'
                
                return {
                    'success': True,
                    'commit_hash': commit_hash,
                    'commit_message': commit_message,
                    'output': commit_result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': commit_result.stderr,
                    'output': commit_result.stdout
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def push_to_remote(self) -> Dict[str, Any]:
        """
        推送到远程仓库
        """
        try:
            print("🚀 推送到远程仓库...")
            
            # 推送到main分支
            push_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                       capture_output=True, text=True, cwd=self.repo_path)
            
            if push_result.returncode == 0:
                print("✅ 成功推送到远程仓库")
                return {
                    'success': True,
                    'message': 'Successfully pushed to remote repository',
                    'output': push_result.stdout
                }
            else:
                # 如果推送失败，可能需要设置上游分支
                if 'no upstream branch' in push_result.stderr:
                    print("🔄 设置上游分支并推送...")
                    upstream_result = subprocess.run(['git', 'push', '--set-upstream', 'origin', 'main'], 
                                                   capture_output=True, text=True, cwd=self.repo_path)
                    if upstream_result.returncode == 0:
                        print("✅ 成功设置上游分支并推送")
                        return {
                            'success': True,
                            'message': 'Successfully set upstream and pushed',
                            'output': upstream_result.stdout
                        }
                    else:
                        return {
                            'success': False,
                            'error': upstream_result.stderr,
                            'output': upstream_result.stdout
                        }
                else:
                    return {
                        'success': False,
                        'error': push_result.stderr,
                        'output': push_result.stdout
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def simulate_gitlab_webhook(self, commit_hash: str) -> Dict[str, Any]:
        """
        模拟GitLab webhook调用
        """
        try:
            print("🔗 模拟GitLab webhook调用...")
            
            # 构造webhook payload
            webhook_payload = {
                "object_kind": "push",
                "event_name": "push",
                "before": "0000000000000000000000000000000000000000",
                "after": commit_hash,
                "ref": "refs/heads/main",
                "checkout_sha": commit_hash,
                "message": "🚨 CRITICAL: 生产环境WAF安全策略紧急变更",
                "user_id": 1,
                "user_name": "ops-team",
                "user_username": "ops-team",
                "user_email": "ops-team@company.com",
                "project_id": int(self.project_id) if self.project_id.isdigit() else 1,
                "project": {
                    "id": int(self.project_id) if self.project_id.isdigit() else 1,
                    "name": "AI Risk Assessment System",
                    "description": "Intelligent risk assessment for infrastructure changes",
                    "web_url": f"{self.gitlab_url}/ai-risk-assessment",
                    "avatar_url": None,
                    "git_ssh_url": "git@gitlab.example.com:security/ai-risk-assessment.git",
                    "git_http_url": f"{self.gitlab_url}/security/ai-risk-assessment.git",
                    "namespace": "security",
                    "visibility_level": 10,
                    "path_with_namespace": "security/ai-risk-assessment",
                    "default_branch": "main",
                    "homepage": f"{self.gitlab_url}/security/ai-risk-assessment",
                    "url": "git@gitlab.example.com:security/ai-risk-assessment.git",
                    "ssh_url": "git@gitlab.example.com:security/ai-risk-assessment.git",
                    "http_url": f"{self.gitlab_url}/security/ai-risk-assessment.git"
                },
                "commits": [
                    {
                        "id": commit_hash,
                        "message": "🚨 CRITICAL: 生产环境WAF安全策略紧急变更\n\n变更类型: 高风险WAF配置调整\n风险等级: CRITICAL",
                        "title": "🚨 CRITICAL: 生产环境WAF安全策略紧急变更",
                        "timestamp": datetime.now().isoformat(),
                        "url": f"{self.gitlab_url}/security/ai-risk-assessment/-/commit/{commit_hash}",
                        "author": {
                            "name": "ops-team",
                            "email": "ops-team@company.com"
                        },
                        "added": [],
                        "modified": [
                            "waf_security_policy_change.yaml",
                            "tencent_waf_api_operations.py"
                        ],
                        "removed": []
                    }
                ],
                "total_commits_count": 1,
                "push_options": {},
                "repository": {
                    "name": "AI Risk Assessment System",
                    "url": "git@gitlab.example.com:security/ai-risk-assessment.git",
                    "description": "Intelligent risk assessment for infrastructure changes",
                    "homepage": f"{self.gitlab_url}/security/ai-risk-assessment",
                    "git_http_url": f"{self.gitlab_url}/security/ai-risk-assessment.git",
                    "git_ssh_url": "git@gitlab.example.com:security/ai-risk-assessment.git",
                    "visibility_level": 10
                }
            }
            
            # 发送webhook请求
            headers = {
                'Content-Type': 'application/json',
                'X-Gitlab-Event': 'Push Hook',
                'X-Gitlab-Token': self.gitlab_token,
                'User-Agent': 'GitLab/14.0.0'
            }
            
            response = requests.post(
                self.webhook_url,
                json=webhook_payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ Webhook调用成功")
                try:
                    response_data = response.json()
                except:
                    response_data = response.text
                    
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'response': response_data,
                    'webhook_payload': webhook_payload
                }
            else:
                print(f"❌ Webhook调用失败: {response.status_code}")
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'error': response.text,
                    'webhook_payload': webhook_payload
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'webhook_payload': webhook_payload if 'webhook_payload' in locals() else None
            }
    
    def execute_full_push_workflow(self) -> Dict[str, Any]:
        """
        执行完整的推送工作流
        """
        print("🚨🚨🚨 开始执行WAF变更推送到GitLab 🚨🚨🚨")
        print(f"推送时间: {datetime.now().isoformat()}")
        print(f"目标分支: main")
        print(f"变更文件: {', '.join(self.change_files)}")
        print("="*80)
        
        workflow_results = {
            'workflow_summary': {
                'timestamp': datetime.now().isoformat(),
                'target_branch': 'main',
                'change_files': self.change_files,
                'total_steps': 5
            },
            'steps': {}
        }
        
        try:
            # 步骤1: 检查Git状态
            print("\n📋 步骤1: 检查Git仓库状态")
            git_status = self.check_git_status()
            workflow_results['steps']['git_status'] = git_status
            
            if not git_status['success']:
                print(f"❌ Git状态检查失败: {git_status['error']}")
                return workflow_results
            
            print(f"✅ 当前分支: {git_status['current_branch']}")
            print(f"📝 未提交文件数: {len(git_status['modified_files'])}")
            
            # 步骤2: 切换到main分支
            print("\n🔄 步骤2: 切换到main分支")
            branch_switch = self.switch_to_main_branch()
            workflow_results['steps']['branch_switch'] = branch_switch
            
            if not branch_switch['success']:
                print(f"❌ 分支切换失败: {branch_switch['error']}")
                return workflow_results
            
            # 步骤3: 添加并提交变更
            print("\n📝 步骤3: 添加并提交变更")
            commit_result = self.add_and_commit_changes()
            workflow_results['steps']['commit'] = commit_result
            
            if not commit_result['success']:
                print(f"❌ 提交失败: {commit_result['error']}")
                return workflow_results
            
            commit_hash = commit_result['commit_hash']
            print(f"✅ 提交哈希: {commit_hash}")
            
            # 步骤4: 推送到远程仓库
            print("\n🚀 步骤4: 推送到远程仓库")
            push_result = self.push_to_remote()
            workflow_results['steps']['push'] = push_result
            
            if not push_result['success']:
                print(f"❌ 推送失败: {push_result['error']}")
                # 即使推送失败，我们仍然可以模拟webhook
            else:
                print("✅ 推送成功")
            
            # 步骤5: 模拟GitLab webhook
            print("\n🔗 步骤5: 触发AI风险评估webhook")
            webhook_result = self.simulate_gitlab_webhook(commit_hash)
            workflow_results['steps']['webhook'] = webhook_result
            
            if webhook_result['success']:
                print("✅ Webhook触发成功")
                print("🤖 AI风险评估系统已开始分析变更")
            else:
                print(f"❌ Webhook触发失败: {webhook_result.get('error', 'Unknown error')}")
            
            print("\n" + "="*80)
            print("🎯 WAF变更推送工作流执行完成！")
            print(f"📋 提交哈希: {commit_hash}")
            print(f"🔗 Webhook状态: {'成功' if webhook_result['success'] else '失败'}")
            print(f"🤖 AI风险评估: {'已触发' if webhook_result['success'] else '未触发'}")
            print("="*80)
            
            return workflow_results
            
        except Exception as e:
            error_result = {
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'partial_results': workflow_results
            }
            print(f"❌ 工作流执行过程中发生错误: {e}")
            return error_result

def main():
    """
    主函数：执行GitLab推送工作流
    """
    print("🚨🚨🚨 WAF高风险变更GitLab推送脚本 🚨🚨🚨")
    print("📋 功能：推送WAF配置变更到GitLab并触发AI风险评估")
    print("🎯 目标分支：main")
    print("🔗 触发：AI风险评估webhook")
    print("⚠️  风险等级：CRITICAL")
    print("\n" + "="*80 + "\n")
    
    # 创建GitLab推送实例
    pusher = GitLabPusher()
    
    # 执行完整推送工作流
    results = pusher.execute_full_push_workflow()
    
    # 保存结果到文件
    output_file = f'gitlab_push_results_{int(time.time())}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 推送结果已保存到: {output_file}")
    
    # 显示关键结果
    if 'steps' in results:
        print("\n🔍 关键结果摘要:")
        
        # 提交结果
        if 'commit' in results['steps'] and results['steps']['commit']['success']:
            print(f"✅ 提交成功: {results['steps']['commit']['commit_hash']}")
        
        # 推送结果
        if 'push' in results['steps']:
            push_status = "✅ 成功" if results['steps']['push']['success'] else "❌ 失败"
            print(f"🚀 推送状态: {push_status}")
        
        # Webhook结果
        if 'webhook' in results['steps']:
            webhook_status = "✅ 成功" if results['steps']['webhook']['success'] else "❌ 失败"
            print(f"🔗 Webhook状态: {webhook_status}")
            
            if results['steps']['webhook']['success']:
                response = results['steps']['webhook'].get('response', {})
                if isinstance(response, dict) and 'risk_assessment' in response:
                    risk_level = response['risk_assessment'].get('overall_risk', 'Unknown')
                    print(f"🤖 AI评估结果: {risk_level}")
    
    return results

if __name__ == '__main__':
    main()