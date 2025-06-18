#!/usr/bin/env python3

from influxdb_client import InfluxDBClient
from datetime import datetime

# InfluxDB 配置
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=="
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "risk_assessment"

def check_data():
    """简单检查 InfluxDB 中的数据"""
    
    print("🔍 检查 InfluxDB 数据...")
    
    try:
        client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        
        query_api = client.query_api()
        
        # 查询最近的所有数据
        print("\n📊 查询最近的风险评估数据:")
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -24h)
        |> filter(fn: (r) => r._measurement == "risk_assessment")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 20)
        '''
        
        result = query_api.query(org=INFLUXDB_ORG, query=query)
        
        if result:
            print("✅ 找到数据:")
            data_count = 0
            for table in result:
                for record in table.records:
                    data_count += 1
                    time_str = record.get_time().strftime('%Y-%m-%d %H:%M:%S')
                    field = record.get_field()
                    value = record.get_value()
                    project = record.values.get('project', 'N/A')
                    commit_id = record.values.get('commit_id', 'N/A')
                    print(f"   [{time_str}] {project}/{commit_id}: {field} = {value}")
            
            print(f"\n📈 总共找到 {data_count} 条数据记录")
            
            # 简单的数据统计
            print("\n📋 数据字段统计:")
            fields = set()
            projects = set()
            for table in result:
                for record in table.records:
                    fields.add(record.get_field())
                    if 'project' in record.values:
                        projects.add(record.values['project'])
            
            print(f"   字段类型: {', '.join(fields)}")
            print(f"   项目: {', '.join(projects)}")
            
        else:
            print("❌ 未找到任何数据")
            print("\n🔧 可能的原因:")
            print("   1. 数据还未写入")
            print("   2. 时间范围不正确")
            print("   3. measurement 名称不匹配")
        
        client.close()
        
        # 提供 Grafana 配置建议
        print("\n🎯 Grafana 配置建议:")
        print("\n1. 数据源配置:")
        print(f"   URL: {INFLUXDB_URL}")
        print(f"   组织: {INFLUXDB_ORG}")
        print(f"   Token: {INFLUXDB_TOKEN}")
        print(f"   默认 Bucket: {INFLUXDB_BUCKET}")
        
        print("\n2. 基础查询示例:")
        basic_query = f'''
from(bucket: "{INFLUXDB_BUCKET}")
|> range(start: $__timeFrom, stop: $__timeTo)
|> filter(fn: (r) => r._measurement == "risk_assessment")
|> filter(fn: (r) => r._field == "risk_probability")
        '''.strip()
        print(f"```flux\n{basic_query}\n```")
        
        print("\n3. 检查步骤:")
        print("   ✓ 确保 Grafana 能连接到 InfluxDB")
        print("   ✓ 验证数据源配置")
        print("   ✓ 使用查询编辑器测试基础查询")
        print("   ✓ 检查时间范围设置")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

if __name__ == "__main__":
    success = check_data()
    if success:
        print("\n✅ 数据检查完成")
    else:
        print("\n❌ 数据检查失败")