#!/usr/bin/env python3
from influxdb_client import InfluxDBClient

def check_influxdb():
    try:
        # 连接InfluxDB
        client = InfluxDBClient(
            url='http://localhost:8086',
            token='A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=='
        )
        
        print("✅ Connected to InfluxDB")
        
        # 检查健康状态
        health = client.health()
        print(f"Health status: {health.status}")
        print(f"Message: {health.message}")
        
        # 获取组织信息
        orgs_api = client.organizations_api()
        orgs = orgs_api.find_organizations()
        
        print(f"\nFound {len(orgs)} organizations:")
        for org in orgs:
            print(f"  - Name: {org.name}")
            print(f"    ID: {org.id}")
            print(f"    Description: {org.description}")
            print()
        
        # 如果有组织，检查buckets
        if orgs:
            first_org = orgs[0]
            print(f"Checking buckets for organization: {first_org.name}")
            
            buckets_api = client.buckets_api()
            buckets = buckets_api.find_buckets(org=first_org.id)
            
            print(f"Found {len(buckets.buckets)} buckets:")
            for bucket in buckets.buckets:
                print(f"  - {bucket.name} (id: {bucket.id})")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_influxdb()