#!/usr/bin/env python3
from influxdb_client import InfluxDBClient

def test_influxdb():
    try:
        # 不指定组织的连接
        client = InfluxDBClient(
            url='http://localhost:8086',
            token='A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=='
        )
        
        print("✅ Connected to InfluxDB")
        
        # 检查健康状态
        health = client.health()
        print(f"Health status: {health.status}")
        print(f"Message: {health.message}")
        
        # 尝试获取组织信息（不使用org参数）
        try:
            orgs_api = client.organizations_api()
            orgs = orgs_api.find_organizations()
            
            print(f"\nFound {len(orgs)} organizations:")
            for org in orgs:
                print(f"  - Name: {org.name}")
                print(f"    ID: {org.id}")
                
                # 尝试获取这个组织的buckets
                try:
                    buckets_api = client.buckets_api()
                    buckets = buckets_api.find_buckets(org=org.id)
                    print(f"    Buckets: {len(buckets.buckets)}")
                    for bucket in buckets.buckets:
                        print(f"      - {bucket.name}")
                except Exception as bucket_error:
                    print(f"    Error getting buckets: {bucket_error}")
                print()
                
        except Exception as org_error:
            print(f"Error getting organizations: {org_error}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_influxdb()