#!/usr/bin/env python3

import requests
import json
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB 配置
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=="
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "risk_assessment"

def setup_influxdb():
    """设置 InfluxDB 组织和 bucket"""
    
    print("🔧 开始设置 InfluxDB...")
    
    # 1. 检查 InfluxDB 健康状态
    try:
        health_response = requests.get(f"{INFLUXDB_URL}/health")
        if health_response.status_code == 200:
            print("✅ InfluxDB 服务正常运行")
        else:
            print(f"❌ InfluxDB 健康检查失败: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到 InfluxDB: {e}")
        return False
    
    # 2. 创建组织
    try:
        org_data = {
            "name": INFLUXDB_ORG,
            "description": "Risk Assessment Organization"
        }
        
        headers = {
            "Authorization": f"Token {INFLUXDB_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # 先检查组织是否已存在
        orgs_response = requests.get(f"{INFLUXDB_URL}/api/v2/orgs", headers=headers)
        if orgs_response.status_code == 200:
            orgs = orgs_response.json().get('orgs', [])
            existing_org = None
            for org in orgs:
                if org['name'] == INFLUXDB_ORG:
                    existing_org = org
                    break
            
            if existing_org:
                print(f"✅ 组织 '{INFLUXDB_ORG}' 已存在 (ID: {existing_org['id']})")
                org_id = existing_org['id']
            else:
                # 创建新组织
                create_org_response = requests.post(
                    f"{INFLUXDB_URL}/api/v2/orgs",
                    headers=headers,
                    json=org_data
                )
                
                if create_org_response.status_code == 201:
                    org_info = create_org_response.json()
                    org_id = org_info['id']
                    print(f"✅ 组织 '{INFLUXDB_ORG}' 创建成功 (ID: {org_id})")
                else:
                    print(f"❌ 创建组织失败: {create_org_response.status_code}")
                    print(f"响应: {create_org_response.text}")
                    return False
        else:
            print(f"❌ 获取组织列表失败: {orgs_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 组织操作失败: {e}")
        return False
    
    # 3. 创建 bucket
    try:
        bucket_data = {
            "name": INFLUXDB_BUCKET,
            "orgID": org_id,
            "description": "Risk Assessment Data Bucket",
            "retentionRules": [
                {
                    "type": "expire",
                    "everySeconds": 2592000  # 30 天
                }
            ]
        }
        
        # 先检查 bucket 是否已存在
        buckets_response = requests.get(
            f"{INFLUXDB_URL}/api/v2/buckets",
            headers=headers,
            params={"orgID": org_id}
        )
        
        if buckets_response.status_code == 200:
            buckets = buckets_response.json().get('buckets', [])
            existing_bucket = None
            for bucket in buckets:
                if bucket['name'] == INFLUXDB_BUCKET:
                    existing_bucket = bucket
                    break
            
            if existing_bucket:
                print(f"✅ Bucket '{INFLUXDB_BUCKET}' 已存在 (ID: {existing_bucket['id']})")
            else:
                # 创建新 bucket
                create_bucket_response = requests.post(
                    f"{INFLUXDB_URL}/api/v2/buckets",
                    headers=headers,
                    json=bucket_data
                )
                
                if create_bucket_response.status_code == 201:
                    bucket_info = create_bucket_response.json()
                    print(f"✅ Bucket '{INFLUXDB_BUCKET}' 创建成功 (ID: {bucket_info['id']})")
                else:
                    print(f"❌ 创建 bucket 失败: {create_bucket_response.status_code}")
                    print(f"响应: {create_bucket_response.text}")
                    return False
        else:
            print(f"❌ 获取 bucket 列表失败: {buckets_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Bucket 操作失败: {e}")
        return False
    
    # 4. 测试数据写入
    try:
        print("🧪 测试数据写入...")
        
        client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        # 写入测试数据
        test_data = f"risk_assessment,project=test-setup,commit_id=setup-test risk_probability=0.5,change_type=\"TEST\" {int(__import__('time').time() * 1000000000)}"
        
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=test_data)
        print("✅ 测试数据写入成功")
        
        # 测试数据查询
        query_api = client.query_api()
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "risk_assessment")
        |> filter(fn: (r) => r.project == "test-setup")
        '''
        
        result = query_api.query(org=INFLUXDB_ORG, query=query)
        
        if result:
            print("✅ 测试数据查询成功")
            for table in result:
                for record in table.records:
                    print(f"   - {record.get_field()}: {record.get_value()}")
        else:
            print("⚠️  查询结果为空，但写入可能成功")
        
        client.close()
        
    except Exception as e:
        print(f"❌ 数据操作测试失败: {e}")
        return False
    
    print("\n🎉 InfluxDB 设置完成!")
    print(f"\n📋 配置信息:")
    print(f"   URL: {INFLUXDB_URL}")
    print(f"   组织: {INFLUXDB_ORG}")
    print(f"   Bucket: {INFLUXDB_BUCKET}")
    print(f"   Token: {INFLUXDB_TOKEN}")
    
    return True

if __name__ == "__main__":
    success = setup_influxdb()
    if success:
        print("\n✅ 现在可以重启 AI 推理服务来使用正确的 InfluxDB 配置")
    else:
        print("\n❌ InfluxDB 设置失败，请检查配置")