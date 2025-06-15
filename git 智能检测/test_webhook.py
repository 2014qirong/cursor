#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_infer_service.main import preprocess_infrastructure_change, match_change_with_knowledge_base
import json

def test_gitlab_webhook_processing():
    """测试 GitLab Webhook 处理功能"""
    
    # 加载知识库
    try:
        with open('ai_infer_service/knowledge_base.json', 'r', encoding='utf-8') as f:
            kb = json.load(f)
    except FileNotFoundError:
        print("知识库文件未找到，使用空知识库")
        kb = {"change_items": []}
    
    # 模拟 GitLab Push Event 数据
    test_commits = [
        {
            'id': 'abc123',
            'message': 'Update NodePool configuration for production cluster',
            'url': 'http://example.com/commit/abc123'
        },
        {
            'id': 'def456', 
            'message': 'Fix database connection timeout',
            'url': 'http://example.com/commit/def456'
        },
        {
            'id': 'ghi789',
            'message': 'Add new OSS bucket permissions for data processing',
            'url': 'http://example.com/commit/ghi789'
        }
    ]
    
    print("=== GitLab Webhook 处理测试 ===")
    print()
    
    for commit in test_commits:
        print(f"提交 ID: {commit['id']}")
        print(f"提交消息: {commit['message']}")
        
        # 预处理基础设施变更
        processed = preprocess_infrastructure_change(commit['message'])
        print(f"预处理结果: {processed}")
        
        # 匹配知识库
        change_type, content = processed
        matched = match_change_with_knowledge_base(change_type, content, kb)
        print(f"知识库匹配: {matched}")
        
        # 检查强制检测模式
        force_detect = False
        if 'kind: NodePool' in commit['message'] or 'NodePool' in commit['message']:
            force_detect = True
            print("触发强制检测: NodePool 相关变更")
        elif 'OSS' in commit['message'] and ('权限' in commit['message'] or 'permission' in commit['message']):
            force_detect = True
            print("触发强制检测: OSS 权限相关变更")
        
        print(f"强制检测模式: {force_detect}")
        print("-" * 50)
        print()

if __name__ == '__main__':
    test_gitlab_webhook_processing()