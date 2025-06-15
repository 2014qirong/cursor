#!/usr/bin/env python3
from influxdb_client import InfluxDBClient, Point, WritePrecision
from datetime import datetime

def test_influxdb_write():
    try:
        # 连接InfluxDB
        client = InfluxDBClient(
            url='http://localhost:8086',
            token='A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw==',
            org='my-org'
        )
        
        write_api = client.write_api()
        
        # 创建测试数据点
        point = Point("risk_assessment") \
            .tag("change_id", "test_123") \
            .tag("impact", "high") \
            .tag("risk_level", "high") \
            .field("probability", 0.8) \
            .field("confidence", 0.9) \
            .time(datetime.utcnow(), WritePrecision.NS)
        
        # 写入数据
        write_api.write(bucket='risk_assessment', org='my-org', record=point)
        print("✅ Data written successfully to InfluxDB")
        
        # 查询数据验证
        query_api = client.query_api()
        query = 'from(bucket: "risk_assessment") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "risk_assessment")'
        result = query_api.query(org='my-org', query=query)
        
        print(f"✅ Query result: {len(result)} tables found")
        for table in result:
            for record in table.records:
                print(f"  - {record.get_field()}: {record.get_value()} (time: {record.get_time()})")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_influxdb_write()