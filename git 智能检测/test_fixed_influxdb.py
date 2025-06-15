#!/usr/bin/env python3
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def test_fixed_influxdb():
    try:
        # 使用正确的组织ID
        client = InfluxDBClient(
            url='http://localhost:8086',
            token='A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=='
        )
        
        print("✅ Connected to InfluxDB")
        
        # 使用组织ID而不是名称
        org_id = "0e99aeecad56cd00"
        bucket = "risk_assessment"
        
        # 创建写入API
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        # 创建测试数据点
        point = Point("test_risk_assessment") \
            .tag("change_id", "test_123") \
            .tag("risk_level", "medium") \
            .field("probability", 0.75) \
            .field("impact", "moderate")
        
        # 写入数据
        write_api.write(bucket=bucket, org=org_id, record=point)
        print("✅ Data written successfully to InfluxDB")
        
        # 验证数据写入
        query_api = client.query_api()
        query = f'''
        from(bucket: "{bucket}")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "test_risk_assessment")
        |> last()
        '''
        
        result = query_api.query(org=org_id, query=query)
        
        if result:
            print("✅ Data verification successful:")
            for table in result:
                for record in table.records:
                    print(f"  - {record.get_field()}: {record.get_value()}")
        else:
            print("⚠️ No data found in query result")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_fixed_influxdb()