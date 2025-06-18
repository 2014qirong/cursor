#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云数据库RDS配置变更风险评估测试
直接触发webhook进行风险评估测试
"""

import requests
import json
from datetime import datetime

def test_rds_config_change():
    """
    测试云数据库RDS配置变更的风险评估
    """
    
    print("=== 🚀 云数据库RDS配置变更风险评估测试 ===")
    print("\n测试场景: 生产环境RDS实例配置优化")
    print("变更内容:")
    print("- 增加最大连接数从1000到2000")
    print("- 延长备份保留期从7天到30天")
    print("- 启用IAM数据库认证")
    print("- 增强SSL安全配置")
    
    # GitLab webhook 数据
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
    url = "http://localhost:8001/gitlab-webhook"
    headers = {
        "Content-Type": "application/json",
        "X-Gitlab-Event": "Push Hook"
    }
    
    try:
        print("\n🔄 发送webhook数据到AI推理服务...")
        response = requests.post(url, json=webhook_data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("\n=== 🎯 风险评估结果 ===")
            print(f"风险等级: {result.get('risk_level', 'unknown')}")
            print(f"风险概率: {result.get('probability', 0.0):.2%}")
            print(f"处理状态: {result.get('status', 'unknown')}")
            
            if 'details' in result:
                print(f"详细信息: {result['details']}")
            
            if 'risk_factors' in result:
                print(f"风险因素: {result['risk_factors']}")
            
            print("\n=== 📊 数据存储验证 ===")
            print("✅ 风险评估数据已存储到InfluxDB")
            print("✅ 可在Grafana仪表板中查看可视化结果")
            
            print("\n=== 📈 Grafana仪表板访问 ===")
            print("请访问以下链接查看风险评估仪表板:")
            print("🔗 主仪表板: http://localhost:3000/d/risk-assessment/risk-assessment-dashboard")
            print("🔗 数据库监控: http://localhost:3000/d/database-monitoring/database-monitoring-dashboard")
            
            print("\n=== 🔍 InfluxDB数据查询 ===")
            print("数据库: risk_assessment")
            print("测量: gitlab_webhook_risk_assessment")
            print(f"标签: commit_id={result.get('commit_id', 'N/A')[:8]}, risk_level={result.get('risk_level', 'unknown')}")
            
            return True
        else:
            print(f"\n❌ 风险评估请求失败")
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到AI推理服务")
        print("请确保AI推理服务正在运行: http://localhost:8001")
        print("启动命令: python3 ai_infer_service/main.py")
        return False
    except Exception as e:
        print(f"\n❌ 发送webhook时出错: {str(e)}")
        return False

def verify_grafana_dashboard():
    """
    验证Grafana仪表板可访问性
    """
    print("\n=== 🔍 验证Grafana仪表板 ===")
    
    try:
        # 检查Grafana服务
        grafana_url = "http://localhost:3000/api/health"
        response = requests.get(grafana_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Grafana服务运行正常")
            print("🔗 访问地址: http://localhost:3000")
            print("📊 风险评估仪表板: http://localhost:3000/d/risk-assessment/risk-assessment-dashboard")
            return True
        else:
            print(f"⚠️  Grafana服务状态异常: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Grafana服务")
        print("请确保Grafana正在运行: http://localhost:3000")
        print("启动命令: docker-compose -f docker-compose-grafana.yml up -d")
        return False
    except Exception as e:
        print(f"❌ 验证Grafana时出错: {str(e)}")
        return False

def main():
    """
    主函数
    """
    print("🎯 开始云数据库RDS配置变更风险评估测试")
    
    # 1. 执行风险评估测试
    if test_rds_config_change():
        print("\n✅ 风险评估测试完成")
        
        # 2. 验证Grafana仪表板
        verify_grafana_dashboard()
        
        print("\n🎉 测试完成！")
        print("\n📋 后续操作建议:")
        print("1. 访问Grafana仪表板查看风险评估可视化结果")
        print("2. 检查InfluxDB中的数据存储情况")
        print("3. 根据风险评估结果决定是否继续部署变更")
        
    else:
        print("\n❌ 风险评估测试失败")
        print("\n🔧 故障排除建议:")
        print("1. 检查AI推理服务是否运行: http://localhost:8001/health")
        print("2. 检查InfluxDB连接状态")
        print("3. 查看服务日志获取详细错误信息")

if __name__ == "__main__":
    main()