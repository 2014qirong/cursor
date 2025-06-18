#!/usr/bin/env python3

import requests
from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta
import json

# InfluxDB 配置
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=="
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "risk_assessment"

def verify_influxdb_data():
    """验证 InfluxDB 中的风险评估数据"""
    
    print("🔍 验证 InfluxDB 数据...")
    
    try:
        client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        
        query_api = client.query_api()
        
        # 1. 查询最近的风险评估数据
        print("\n📊 查询最近的风险评估数据:")
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -24h)
        |> filter(fn: (r) => r._measurement == "risk_assessment")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 10)
        '''
        
        result = query_api.query(org=INFLUXDB_ORG, query=query)
        
        if result:
            print("✅ 找到风险评估数据:")
            for table in result:
                for record in table.records:
                    time_str = record.get_time().strftime('%Y-%m-%d %H:%M:%S')
                    field = record.get_field()
                    value = record.get_value()
                    project = record.values.get('project', 'N/A')
                    commit_id = record.values.get('commit_id', 'N/A')
                    print(f"   [{time_str}] {project}/{commit_id}: {field} = {value}")
        else:
            print("❌ 未找到风险评估数据")
        
        # 2. 统计数据概览
        print("\n📈 数据统计概览:")
        stats_query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -24h)
        |> filter(fn: (r) => r._measurement == "risk_assessment")
        |> filter(fn: (r) => r._field == "risk_probability")
        |> group(columns: ["project"])
        |> count()
        '''
        
        stats_result = query_api.query(org=INFLUXDB_ORG, query=stats_query)
        
        if stats_result:
            print("✅ 项目统计:")
            for table in stats_result:
                for record in table.records:
                    project = record.values.get('project', 'N/A')
                    count = record.get_value()
                    print(f"   项目 {project}: {count} 条记录")
        
        # 3. 风险等级分布
        print("\n🎯 风险等级分布:")
        risk_query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -24h)
        |> filter(fn: (r) => r._measurement == "risk_assessment")
        |> filter(fn: (r) => r._field == "change_type")
        |> group(columns: ["_value"])
        |> count()
        '''
        
        risk_result = query_api.query(org=INFLUXDB_ORG, query=risk_query)
        
        if risk_result:
            print("✅ 变更类型分布:")
            for table in risk_result:
                for record in table.records:
                    change_type = record.get_value()
                    count = record.values.get('_value', 0)
                    print(f"   {change_type}: {count} 次")
        
        # 4. 生成 Grafana 查询示例
        print("\n📋 Grafana 查询示例:")
        grafana_queries = {
            "风险概率时间序列": f'''
from(bucket: "{INFLUXDB_BUCKET}")
|> range(start: $__timeFrom, stop: $__timeTo)
|> filter(fn: (r) => r._measurement == "risk_assessment")
|> filter(fn: (r) => r._field == "risk_probability")
|> aggregateWindow(every: $__interval, fn: mean, createEmpty: false)
|> yield(name: "mean")
            '''.strip(),
            
            "项目风险分布": f'''
from(bucket: "{INFLUXDB_BUCKET}")
|> range(start: $__timeFrom, stop: $__timeTo)
|> filter(fn: (r) => r._measurement == "risk_assessment")
|> filter(fn: (r) => r._field == "risk_probability")
|> group(columns: ["project"])
|> mean()
|> yield(name: "mean")
            '''.strip(),
            
            "变更类型统计": f'''
from(bucket: "{INFLUXDB_BUCKET}")
|> range(start: $__timeFrom, stop: $__timeTo)
|> filter(fn: (r) => r._measurement == "risk_assessment")
|> filter(fn: (r) => r._field == "change_type")
|> group(columns: ["_value"])
|> count()
|> yield(name: "count")
            '''.strip()
        }
        
        for name, query in grafana_queries.items():
            print(f"\n🔹 {name}:")
            print(f"```flux\n{query}\n```")
        
        client.close()
        
        print("\n🎉 InfluxDB 数据验证完成!")
        print("\n💡 提示:")
        print("   1. 确保 Grafana 数据源配置正确")
        print("   2. 使用上述查询示例创建面板")
        print("   3. 检查时间范围设置")
        print("   4. 验证字段名称匹配")
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    success = verify_influxdb_data()
    if success:
        print("\n✅ 数据验证成功，可以在 Grafana 中查看数据")
    else:
        print("\n❌ 数据验证失败，请检查配置")