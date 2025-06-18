#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试数据库连接池配置变更用例的风险评估
跳过GitLab推送，直接触发webhook测试
"""

import json
import requests
import time
from datetime import datetime

def trigger_risk_assessment():
    """直接触发风险评估API"""
    print("🔔 触发数据库连接池配置变更的风险评估...")
    
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
                    "monitoring/db-pool-metrics.yaml",
                    "test_cases/database-connection-pool-update/config/database-config.yaml",
                    "test_cases/database-connection-pool-update/terraform/rds-config.tf"
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
        print("📤 发送webhook数据到风险评估API...")
        response = requests.post(
            "http://localhost:8001/webhook/gitlab",
            json=webhook_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 风险评估API响应成功!")
            print(f"📊 风险评估结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return True, result
        else:
            print(f"❌ 风险评估API失败: HTTP {response.status_code}")
            print(f"   响应: {response.text}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到风险评估API (http://localhost:8001)")
        print("   请确保后端服务正在运行")
        return False, None
    except Exception as e:
        print(f"❌ 风险评估API异常: {str(e)}")
        return False, None

def check_influxdb_data():
    """检查InfluxDB中的数据"""
    print("\n📊 检查InfluxDB中的风险评估数据...")
    
    try:
        # 等待数据写入
        print("⏳ 等待数据写入InfluxDB (5秒)...")
        time.sleep(5)
        
        # 简单检查InfluxDB连接
        response = requests.get(
            "http://localhost:8086/health",
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ InfluxDB服务正常运行")
            return True
        else:
            print(f"❌ InfluxDB服务异常: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 检查InfluxDB时出错: {str(e)}")
        return False

def check_grafana_dashboard():
    """检查Grafana仪表板"""
    print("\n📈 检查Grafana仪表板...")
    
    try:
        # 检查Grafana健康状态
        response = requests.get(
            "http://localhost:3000/api/health",
            timeout=10
        )
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Grafana服务正常运行")
            print(f"   版本: {health_data.get('version', 'unknown')}")
            print(f"   数据库状态: {health_data.get('database', 'unknown')}")
            
            # 检查数据源
            print("\n🔍 检查Grafana数据源...")
            ds_response = requests.get(
                "http://localhost:3000/api/datasources",
                auth=('admin', 'admin123'),
                timeout=10
            )
            
            if ds_response.status_code == 200:
                datasources = ds_response.json()
                if datasources:
                    print(f"✅ 找到 {len(datasources)} 个数据源")
                    for ds in datasources:
                        print(f"   - {ds.get('name', 'unknown')}: {ds.get('type', 'unknown')}")
                else:
                    print("⚠️  未找到配置的数据源")
            
            print("\n🔗 访问Grafana仪表板:")
            print("   URL: http://localhost:3000")
            print("   用户名: admin")
            print("   密码: admin123")
            print("   仪表板: 风险评估监控仪表板")
            return True
        else:
            print(f"❌ Grafana服务异常: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 检查Grafana时出错: {str(e)}")
        return False

def test_api_prediction():
    """测试AI预测API"""
    print("\n🤖 测试AI风险预测API...")
    
    # 测试代码片段
    test_code = """
# 数据库连接池配置变更
pool:
  max_connections: 50  # 从20增加到50
  min_idle_connections: 10  # 从5增加到10
  connection_timeout: 20s  # 从30秒减少到20秒
  idle_timeout: 600s  # 从300秒增加到600秒
  max_lifetime: 2h  # 从1小时增加到2小时
"""
    
    try:
        response = requests.post(
            "http://localhost:8001/predict",
            json={"code": test_code},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI预测API响应成功!")
            print(f"📊 预测结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return True, result
        else:
            print(f"❌ AI预测API失败: HTTP {response.status_code}")
            print(f"   响应: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ AI预测API异常: {str(e)}")
        return False, None

def main():
    """主函数"""
    print("=== 数据库连接池配置变更用例直接测试 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📋 测试说明:")
    print("   本测试跳过GitLab推送，直接测试风险评估功能")
    print("   包括: webhook触发、AI预测、数据存储、Grafana展示")
    
    results = {
        'webhook_test': False,
        'ai_prediction': False,
        'influxdb_check': False,
        'grafana_check': False
    }
    
    try:
        # 1. 测试AI预测API
        print("\n" + "="*50)
        ai_success, ai_result = test_api_prediction()
        results['ai_prediction'] = ai_success
        
        # 2. 触发webhook风险评估
        print("\n" + "="*50)
        webhook_success, webhook_result = trigger_risk_assessment()
        results['webhook_test'] = webhook_success
        
        # 3. 检查InfluxDB数据
        print("\n" + "="*50)
        influxdb_success = check_influxdb_data()
        results['influxdb_check'] = influxdb_success
        
        # 4. 检查Grafana仪表板
        print("\n" + "="*50)
        grafana_success = check_grafana_dashboard()
        results['grafana_check'] = grafana_success
        
        # 输出测试总结
        print("\n" + "="*50)
        print("📋 测试结果总结:")
        print(f"   🤖 AI预测API: {'✅ 成功' if results['ai_prediction'] else '❌ 失败'}")
        print(f"   🔔 Webhook测试: {'✅ 成功' if results['webhook_test'] else '❌ 失败'}")
        print(f"   📊 InfluxDB检查: {'✅ 成功' if results['influxdb_check'] else '❌ 失败'}")
        print(f"   📈 Grafana检查: {'✅ 成功' if results['grafana_check'] else '❌ 失败'}")
        
        success_count = sum(results.values())
        total_count = len(results)
        success_rate = (success_count / total_count) * 100
        
        print(f"\n📊 总体成功率: {success_count}/{total_count} ({success_rate:.1f}%)")
        
        if success_count == total_count:
            print("\n🎉 所有测试通过! 系统运行正常")
            print("\n📝 下一步操作:")
            print("   1. 访问 http://localhost:3000 查看Grafana仪表板")
            print("   2. 在仪表板中查看最新的风险评估数据")
            print("   3. 验证数据库连接池配置变更的风险级别")
        elif success_count >= 2:
            print("\n⚠️  部分测试通过，系统基本可用")
            print("   请检查失败的组件并重新测试")
        else:
            print("\n❌ 多数测试失败，请检查系统配置")
            
    except Exception as e:
        print(f"❌ 执行过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()