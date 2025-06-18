#!/usr/bin/env python3
import requests
import json
from influxdb_client import InfluxDBClient

def check_influxdb_status():
    """检查 InfluxDB 状态和配置"""
    url = "http://localhost:8086"
    token = "A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=="
    
    try:
        # 检查 InfluxDB 健康状态
        health_response = requests.get(f"{url}/health")
        print(f"InfluxDB 健康状态: {health_response.status_code}")
        
        # 使用 InfluxDB 客户端
        client = InfluxDBClient(url=url, token=token)
        
        # 获取所有组织
        orgs_api = client.organizations_api()
        orgs = orgs_api.find_organizations()
        
        print(f"\n找到 {len(orgs)} 个组织:")
        for org in orgs:
            print(f"  - 名称: {org.name}, ID: {org.id}")
        
        if not orgs:
            print("❌ 没有找到任何组织")
            return None, None
        
        # 使用第一个组织
        target_org = orgs[0]
        print(f"\n✅ 使用组织: {target_org.name} (ID: {target_org.id})")
        
        # 获取 buckets
        buckets_api = client.buckets_api()
        buckets = buckets_api.find_buckets(org=target_org.id)
        
        print(f"\n找到 {len(buckets.buckets)} 个 bucket:")
        for bucket in buckets.buckets:
            print(f"  - 名称: {bucket.name}, ID: {bucket.id}")
        
        # 检查是否存在 risk_assessment bucket
        risk_bucket = None
        for bucket in buckets.buckets:
            if bucket.name == "risk_assessment":
                risk_bucket = bucket
                break
        
        if not risk_bucket:
            print("\n创建 risk_assessment bucket...")
            from influxdb_client.domain.bucket import Bucket
            from influxdb_client.domain.bucket_retention_rules import BucketRetentionRules
            
            bucket = Bucket(
                name="risk_assessment",
                org_id=target_org.id,
                retention_rules=[
                    BucketRetentionRules(
                        type="expire",
                        every_seconds=2592000  # 30 days
                    )
                ]
            )
            
            risk_bucket = buckets_api.create_bucket(bucket=bucket)
            print(f"✅ 创建了 bucket: {risk_bucket.name}")
        else:
            print(f"✅ 找到 risk_assessment bucket: {risk_bucket.id}")
        
        return target_org, risk_bucket
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None, None

def update_config_file(org_name, bucket_name):
    """更新配置信息"""
    print(f"\n建议的配置:")
    print(f"INFLUXDB_ORG = '{org_name}'")
    print(f"INFLUXDB_BUCKET = '{bucket_name}'")
    print(f"INFLUXDB_URL = 'http://localhost:8086'")
    print(f"INFLUXDB_TOKEN = 'A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=='")

if __name__ == "__main__":
    print("🔍 检查 InfluxDB 配置...")
    org, bucket = check_influxdb_status()
    
    if org and bucket:
        update_config_file(org.name, bucket.name)
        print("\n✅ InfluxDB 配置检查完成")
    else:
        print("\n❌ InfluxDB 配置检查失败")