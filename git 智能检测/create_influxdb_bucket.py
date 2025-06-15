#!/usr/bin/env python3
from influxdb_client import InfluxDBClient

def create_bucket():
    try:
        # 连接InfluxDB
        client = InfluxDBClient(
            url='http://localhost:8086',
            token='A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw==',
            org='my-org'
        )
        
        # 获取组织信息
        orgs_api = client.organizations_api()
        orgs = orgs_api.find_organizations()
        
        print(f"Found {len(orgs)} organizations:")
        for org in orgs:
            print(f"  - {org.name} (id: {org.id})")
        
        # 查找组织
        my_org = None
        for org in orgs:
            if org.name == 'my-org':
                my_org = org
                break
        
        if not my_org:
            print("❌ Organization 'my-org' not found")
            # 尝试使用第一个可用的组织
            if orgs:
                my_org = orgs[0]
                print(f"Using first available organization: {my_org.name}")
            else:
                print("No organizations found")
                return False
        else:
            print(f"✅ Found organization: {my_org.name}")
        
        # 获取bucket API
        buckets_api = client.buckets_api()
        
        # 检查是否已存在bucket
        existing_buckets = buckets_api.find_buckets(org=my_org.id)
        print(f"\nFound {len(existing_buckets.buckets)} existing buckets:")
        for bucket in existing_buckets.buckets:
            print(f"  - {bucket.name}")
        
        # 检查risk_assessment bucket是否存在
        risk_bucket = None
        for bucket in existing_buckets.buckets:
            if bucket.name == 'risk_assessment':
                risk_bucket = bucket
                break
        
        if not risk_bucket:
            print("\nCreating 'risk_assessment' bucket...")
            # 创建bucket（简化版本）
            bucket_request = {
                "name": "risk_assessment",
                "orgID": my_org.id,
                "retentionRules": [
                    {
                        "type": "expire",
                        "everySeconds": 2592000  # 30天
                    }
                ]
            }
            risk_bucket = buckets_api.create_bucket(bucket=bucket_request)
            print(f"✅ Created bucket: {risk_bucket.name}")
        else:
            print(f"✅ Found existing bucket: {risk_bucket.name}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_bucket()