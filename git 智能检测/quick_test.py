#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 不中断AI服务
"""

import requests
import json
import time

def quick_health_check():
    """快速健康检查"""
    try:
        response = requests.get("http://localhost:8001/health", timeout=3)
        if response.status_code == 200:
            print("✅ AI服务健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {str(e)}")
        return False

def quick_predict_test():
    """快速预测测试"""
    test_data = {
        "code": "# 数据库连接池配置\npool:\n  max_connections: 50\n  timeout: 30"
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/predict",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI预测测试通过")
            print(f"   风险等级: {result.get('risk_level', 'unknown')}")
            print(f"   置信度: {result.get('confidence', 'unknown')}")
            return True
        else:
            print(f"❌ 预测测试失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 预测测试异常: {str(e)}")
        return False

def quick_influxdb_check():
    """快速InfluxDB检查"""
    try:
        import influxdb_client
        
        client = influxdb_client.InfluxDBClient(
            url="http://localhost:8086",
            token="A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw==",
            org="my-org"
        )
        
        # 简单查询测试
        query_api = client.query_api()
        query = 'from(bucket:"risk_assessment") |> range(start: -1h) |> limit(n:1)'
        
        result = query_api.query(query=query)
        print("✅ InfluxDB连接正常")
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ InfluxDB检查失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== 快速系统测试 ===")
    
    results = []
    
    # 1. 健康检查
    print("\n🔍 AI服务健康检查...")
    results.append(quick_health_check())
    
    # 2. 预测测试
    print("\n🔍 AI预测功能测试...")
    results.append(quick_predict_test())
    
    # 3. InfluxDB检查
    print("\n🔍 InfluxDB连接测试...")
    results.append(quick_influxdb_check())
    
    # 总结
    success_count = sum(results)
    total_count = len(results)
    success_rate = (success_count / total_count) * 100
    
    print("\n" + "="*40)
    print(f"📊 测试结果: {success_count}/{total_count} ({success_rate:.1f}%)")
    
    if success_count == total_count:
        print("🎉 所有测试通过！系统运行正常")
    elif success_count >= 2:
        print("⚠️  部分功能正常，系统基本可用")
    else:
        print("❌ 系统存在严重问题")