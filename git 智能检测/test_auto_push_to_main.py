#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自动推送到主干分支功能
验证GitLab自动推送规则是否正常工作
"""

import os
import sys
from datetime import datetime
from push_to_gitlab import GitLabPusher

def test_auto_push_to_main():
    """测试自动推送到主干分支"""
    
    print("🧪 开始测试自动推送到主干分支功能")
    print("=" * 50)
    
    # 检查环境变量
    print("📋 检查环境变量配置:")
    gitlab_url = os.getenv('GITLAB_URL')
    project_id = os.getenv('GITLAB_PROJECT_ID')
    username = os.getenv('GITLAB_USERNAME')
    password = os.getenv('GITLAB_PASSWORD')
    auto_push = os.getenv('GITLAB_AUTO_PUSH_TO_MAIN')
    skip_confirm = os.getenv('GITLAB_SKIP_CONFIRMATION')
    default_branch = os.getenv('GITLAB_DEFAULT_BRANCH')
    
    print(f"   GITLAB_URL: {gitlab_url}")
    print(f"   GITLAB_PROJECT_ID: {project_id}")
    print(f"   GITLAB_USERNAME: {username}")
    print(f"   GITLAB_AUTO_PUSH_TO_MAIN: {auto_push}")
    print(f"   GITLAB_SKIP_CONFIRMATION: {skip_confirm}")
    print(f"   GITLAB_DEFAULT_BRANCH: {default_branch}")
    
    if not all([gitlab_url, project_id, username, password]):
        print("❌ GitLab环境变量未正确设置，请先运行: source gitlab_config.sh")
        return False
    
    # 创建GitLab推送器
    print("\n🔧 创建GitLab推送器...")
    try:
        pusher = GitLabPusher(gitlab_url, project_id, username=username, password=password)
        print(f"   自动推送到主干: {pusher.auto_push_to_main}")
        print(f"   跳过确认: {pusher.skip_confirmation}")
        print(f"   默认分支: {pusher.default_branch}")
    except Exception as e:
        print(f"❌ 创建GitLab推送器失败: {e}")
        return False
    
    # 创建测试用例
    print("\n📝 创建测试用例...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    test_case = {
        'test_name': f'自动推送测试_{timestamp}',
        'risk_level': 'LOW',
        'description': '测试自动推送到主干分支功能',
        'files_changed': [f'test_files/auto_push_test_{timestamp}.md'],
        'diff_content': f'''# 自动推送测试文件

## 测试信息
- 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 测试目的: 验证自动推送到主干分支功能
- 风险等级: LOW

## 测试内容
这是一个自动生成的测试文件，用于验证GitLab自动推送规则。

### 配置验证
- 自动推送到主干: {pusher.auto_push_to_main}
- 跳过确认: {pusher.skip_confirmation}
- 目标分支: {pusher.default_branch}

### 推送时间
{datetime.now().isoformat()}
''',
        'commit_message': f'test: 自动推送功能测试 - {timestamp}',
        'author': 'auto-push-test'
    }
    
    # 执行推送测试
    print("\n🚀 执行推送测试...")
    try:
        if pusher.auto_push_to_main:
            print("   ✅ 检测到自动推送模式已启用")
            result = pusher.push_test_case(test_case)
        else:
            print("   ⚠️  自动推送模式未启用，将使用常规分支模式")
            result = pusher.push_test_case(test_case)
        
        if result:
            print("   ✅ 推送测试成功")
            return True
        else:
            print("   ❌ 推送测试失败")
            return False
            
    except Exception as e:
        print(f"   ❌ 推送测试异常: {e}")
        return False

def main():
    """主函数"""
    print("GitLab 自动推送到主干分支 - 功能测试")
    print("=" * 60)
    
    # 检查是否已加载环境变量
    if not os.getenv('GITLAB_URL'):
        print("⚠️  请先加载GitLab配置:")
        print("   source gitlab_config.sh")
        print("   python3 test_auto_push_to_main.py")
        sys.exit(1)
    
    # 执行测试
    success = test_auto_push_to_main()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 自动推送到主干分支功能测试通过！")
        print("\n📋 后续使用说明:")
        print("   1. 确