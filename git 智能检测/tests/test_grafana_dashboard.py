import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB 配置
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=="
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "risk_assessment"

# 连接 InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_test_data():
    """写入测试数据到 InfluxDB"""
    # CDN 风险数据示例
    cdn_risk_data = [
        Point("risk_assessment")
        .tag("change_type", "cdn_config")
        .tag("knowledge_base_type", "CDN")
        .field("description", "禁用WAF防护")
        .field("risk_level", "高")
        .field("probability", 0.85)
        .field("suggestions", "启用备用安全服务, 加强监控和告警")
        .field("cloud_providers", "AWS,AliCloud")
        .field("assessment_factors", "当前安全威胁等级,流量来源分析")
        .field("key_metrics", "恶意请求拦截率,安全事件数量")
        .field("checklist", "确认是否有其他安全防护措施,评估当前威胁环境")
        .field("potential_impacts", "暴露于网络攻击,数据泄露风险")
        .field("mitigation_strategies", "启用备用安全服务,加强监控和告警")
        .field("matched_pattern", "禁用WAF防护规则")
        .field("pattern_source", "cdn_risk_patterns.json")
        .field("similarity", 0.95)
        .time(int(time.time() * 1000), WritePrecision.MS)
    ]
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=cdn_risk_data)
    print(f"成功写入 {len(cdn_risk_data)} 条 CDN 风险数据到 InfluxDB.")

    # 云变更风险数据示例
    cloud_change_risk_data = [
        Point("risk_assessment")
        .tag("change_type", "route53_dns_change")
        .tag("knowledge_base_type", "CloudChange")
        .field("description", "AWS Route53 DNS记录变更")
        .field("risk_level", "高")
        .field("probability", 0.75)
        .field("suggestions", "分阶段切换, 降低TTL")
        .field("cloud_providers", "AWS")
        .field("assessment_factors", "DNS传播时间,TTL设置")
        .field("key_metrics", "DNS解析成功率,响应时间")
        .field("checklist", "确认新记录正确性,评估TTL影响")
        .field("potential_impacts", "服务不可访问,流量丢失")
        .field("mitigation_strategies", "分阶段切换,监控DNS解析")
        .field("matched_pattern", "Route53记录修改")
        .field("pattern_source", "cloud_change_risk_assessment_kb.json")
        .field("similarity", 0.92)
        .time(int(time.time() * 1000) + 1000, WritePrecision.MS) # 确保时间戳不同
    ]
    write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=cloud_change_risk_data)
    print(f"成功写入 {len(cloud_change_risk_data)} 条云变更风险数据到 InfluxDB.")

if __name__ == "__main__":
    print("开始写入测试数据...")
    write_test_data()
    print("测试数据写入完成。请检查 Grafana 仪表盘。")
    print(f"请确保您的 InfluxDB 服务正在运行于: {INFLUXDB_URL}")
    print(f"并且 Token, Org, Bucket 配置正确: Token='your-influxdb-token', Org='{INFLUXDB_ORG}', Bucket='{INFLUXDB_BUCKET}'")
    print("如果仪表盘没有显示数据，请检查 InfluxDB 连接配置和数据写入情况。")