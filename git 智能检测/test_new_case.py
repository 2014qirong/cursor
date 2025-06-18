#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新创建的K8S节点池扩容案例
直接向AI推理服务发送webhook数据
"""

import requests
import json
from datetime import datetime

def test_k8s_nodepool_case():
    """测试K8S节点池扩容案例"""
    
    # AI推理服务地址
    ai_service_url = "http://localhost:8001"
    
    # 构造GitLab webhook数据
    webhook_data = {
        "object_kind": "push",
        "event_name": "push",
        "before": "0000000000000000000000000000000000000000",
        "after": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
        "ref": "refs/heads/test/高风险---k8s集群节点池扩容",
        "checkout_sha": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
        "message": "test: 高风险 - K8S集群节点池扩容",
        "user_id": 1,
        "user_name": "test-automation",
        "user_username": "test-automation",
        "user_email": "test@example.com",
        "user_avatar": "",
        "project_id": 1,
        "project": {
            "id": 1,
            "name": "risk_detect",
            "description": "云变更风险检测系统",
            "web_url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect",
            "avatar_url": None,
            "git_ssh_url": "git@10.251.0.16:risk_detect.git",
            "git_http_url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect.git",
            "namespace": "root",
            "visibility_level": 0,
            "path_with_namespace": "root/risk_detect",
            "default_branch": "main",
            "ci_config_path": None,
            "homepage": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect",
            "url": "git@10.251.0.16:risk_detect.git",
            "ssh_url": "git@10.251.0.16:risk_detect.git",
            "http_url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect.git"
        },
        "commits": [
            {
                "id": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
                "message": "test: 高风险 - K8S集群节点池扩容\n\n- 节点数量从5扩容到8\n- 实例类型: ecs.c6.2xlarge\n- 启用自动伸缩\n- 生产环境变更",
                "title": "test: 高风险 - K8S集群节点池扩容",
                "timestamp": datetime.now().isoformat(),
                "url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect/-/commit/da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
                "author": {
                    "name": "test-automation",
                    "email": "test@example.com"
                },
                "added": [
                    "k8s/nodepool-config.yaml"
                ],
                "modified": [],
                "removed": []
            }
        ],
        "total_commits_count": 1,
        "push_options": {},
        "repository": {
            "name": "risk_detect",
            "url": "git@10.251.0.16:risk_detect.git",
            "description": "云变更风险检测系统",
            "homepage": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect",
            "git_http_url": "http://10.251.0.16/gitlab-instance-1807000d/risk_detect.git",
            "git_ssh_url": "git@10.251.0.16:risk_detect.git",
            "visibility_level": 0
        }
    }
    
    # 发送webhook请求
    try:
        print(f"🚀 向AI推理服务发送K8S节点池扩容测试数据...")
        print(f"服务地址: {ai_service_url}/gitlab-webhook")
        print(f"分支: {webhook_data['ref']}")
        print(f"提交信息: {webhook_data['message']}")
        print()
        
        response = requests.post(
            f"{ai_service_url}/gitlab-webhook",
            json=webhook_data,
            headers={
                "Content-Type": "application/json",
                "X-Gitlab-Event": "Push Hook"
            },
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ 测试成功!")
            print(f"风险评估结果:")
            print(f"  - 风险等级: {result.get('risk_level', 'unknown')}")
            print(f"  - 风险概率: {result.get('risk_probability', 0):.2%}")
            print(f"  - 处理状态: {result.get('status', 'unknown')}")
            
            # 检查是否有风险详情
            if 'risk_details' in result:
                details = result['risk_details']
                print(f"  - 风险描述: {details.get('description', 'N/A')}")
                print(f"  - 影响范围: {details.get('impact', 'N/A')}")
                
            return True
        else:
            print(f"\n❌ 测试失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("K8S节点池扩容风险检测测试")
    print("=" * 60)
    
    success = test_k8s_nodepool_case()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 测试完成，请检查Grafana仪表板中的风险数据显示")
        print("📊 Grafana地址: http://localhost:3000")
        print("📈 仪表板: Risk Assessment Dashboard")
    else:
        print("❌ 测试失败，请检查AI推理服务状态")
    print("=" * 60)

if __name__ == "__main__":
    main()