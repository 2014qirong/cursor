#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合测试脚本 - 验证多种风险场景
生成不同类型的测试数据用于验证系统功能
"""

import requests
import json
import time
import random
from datetime import datetime

# 服务配置
AI_INFER_SERVICE_URL = "http://localhost:8001"

# 测试用例数据
test_cases = [
    {
        "name": "高风险 - Kubernetes 部署变更",
        "webhook_type": "gitlab",
        "data": {
            "object_kind": "push",
            "event_name": "push",
            "project_id": 101,
            "project": {
                "id": 101,
                "name": "k8s-production",
                "namespace": "production"
            },
            "commits": [{
                "id": "k8s001",
                "message": "Update production deployment replicas from 3 to 10",
                "author": {"name": "DevOps Team"},
                "added": ["deployment.yaml"],
                "modified": ["k8s/production/app-deployment.yaml"],
                "removed": []
            }]
        }
    },
    {
        "name": "中风险 - 数据库配置变更",
        "webhook_type": "gitlab",
        "data": {
            "object_kind": "push",
            "event_name": "push",
            "project_id": 102,
            "project": {
                "id": 102,
                "name": "database-config",
                "namespace": "infrastructure"
            },
            "commits": [{
                "id": "db001",
                "message": "Increase database connection pool size",
                "author": {"name": "DBA Team"},
                "added": [],
                "modified": ["config/database.yml", "terraform/rds.tf"],
                "removed": []
            }]
        }
    },
    {
        "name": "低风险 - 文档更新",
        "webhook_type": "gitlab",
        "data": {
            "object_kind": "push",
            "event_name": "push",
            "project_id": 103,
            "project": {
                "id": 103,
                "name": "documentation",
                "namespace": "docs"
            },
            "commits": [{
                "id": "doc001",
                "message": "Update API documentation",
                "author": {"name": "Tech Writer"},
                "added": ["docs/api-v2.md"],
                "modified": ["README.md"],
                "removed": ["docs/deprecated-api.md"]
            }]
        }
    },
    {
        "name": "高风险 - 网络安全组变更",
        "webhook_type": "clb",
        "data": {
            "eventName": "ModifySecurityGroupRules",
            "eventTime": datetime.now().isoformat(),
            "userIdentity": {
                "type": "Root",
                "principalId": "admin-user",
                "arn": "qcs::cam::uin/123456789:root",
                "accountId": "123456789"
            },
            "eventRegion": "ap-beijing",
            "sourceIPAddress": "203.0.113.1",
            "userAgent": "TencentCloud-SDK",
            "requestParameters": {
                "SecurityGroupId": "sg-12345678",
                "SecurityGroupRuleSet": [
                    {
                        "IpProtocol": "TCP",
                        "Port": "22",
                        "CidrBlock": "0.0.0.0/0",
                        "Action": "ACCEPT"
                    }
                ]
            },
            "responseElements": {
                "requestId": "req-12345678"
            }
        }
    },
    {
        "name": "中风险 - 负载均衡器配置",
        "webhook_type": "clb",
        "data": {
            "eventName": "ModifyLoadBalancerAttributes",
            "eventTime": datetime.now().isoformat(),
            "userIdentity": {
                "type": "IAMUser",
                "principalId": "ops-user",
                "arn": "qcs::cam::uin/123456789:user/ops-user",
                "accountId": "123456789"
            },
            "eventRegion": "ap-shanghai",
            "sourceIPAddress": "192.168.1.100",
            "userAgent": "Console",
            "requestParameters": {
                "LoadBalancerId": "lb-12345678",
                "LoadBalancerName": "production-lb",
                "InternetAccessible": {
                    "InternetChargeType": "TRAFFIC_POSTPAID_BY_HOUR",
                    "InternetMaxBandwidthOut": 100
                }
            }
        }
    }
]

def test_webhook(test_case):
    """测试单个webhook用例"""
    print(f"\n🧪 测试用例: {test_case['name']}")
    
    webhook_type = test_case['webhook_type']
    if webhook_type == 'gitlab':
        endpoint = f"{AI_INFER_SERVICE_URL}/gitlab-webhook"
    elif webhook_type == 'clb':
        endpoint = f"{AI_INFER_SERVICE_URL}/clb-webhook"
    else:
        endpoint = f"{AI_INFER_SERVICE_URL}/webhook/{webhook_type}"
    
    try:
        response = requests.post(
            endpoint,
            json=test_case['data'],
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 测试成功")
            
            # 提取风险信息
            if webhook_type == 'gitlab' and 'risk_assessments' in result:
                for assessment in result['risk_assessments']:
                    print(f"   风险等级: {assessment.get('risk_level', 'N/A')}")
                    print(f"   风险概率: {assessment.get('probability', 'N/A')}")
                    print(f"   变更类型: {assessment.get('change_type', 'N/A')}")
            elif webhook_type == 'clb' and 'risk_assessments' in result:
                for assessment in result['risk_assessments']:
                    print(f"   风险等级: {assessment.get('risk_level', 'N/A')}")
                    print(f"   风险概率: {assessment.get('risk_probability', 'N/A')}")
                    print(f"   事件类型: {assessment.get('event_name', 'N/A')}")
            
            return True
        else:
            print(f"❌ 测试失败: HTTP {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def run_comprehensive_tests():
    """运行综合测试"""
    print("🚀 开始综合测试验证")
    print(f"目标服务: {AI_INFER_SERVICE_URL}")
    print("=" * 60)
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/{total_count}] 执行测试...")
        
        if test_webhook(test_case):
            success_count += 1
        
        # 在测试之间添加短暂延迟
        if i < total_count:
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果汇总:")
    print(f"   总测试数: {total_count}")
    print(f"   成功数: {success_count}")
    print(f"   失败数: {total_count - success_count}")
    print(f"   成功率: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 所有测试用例均通过!")
        print("✅ 系统功能验证完成")
        print("\n💡 建议检查:")
        print("   1. Grafana仪表板是否显示新数据")
        print("   2. InfluxDB中的数据是否正确存储")
        print("   3. 不同风险等级的数据分布")
    else:
        print(f"\n⚠️  有 {total_count - success_count} 个测试用例失败")
        print("请检查服务状态和配置")

if __name__ == "__main__":
    run_comprehensive_tests()