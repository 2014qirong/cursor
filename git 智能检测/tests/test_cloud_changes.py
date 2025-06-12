import requests
import json
import time

# 测试用例1：Kubernetes部署变更（高风险）
k8s_deployment_diff = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: production
  labels:
    app: order-service
    env: production
spec:
  replicas: 10  # 从3副本增加到10副本
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # 确保零停机部署
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: company/order-service:v2.5.0  # 从v2.4.3升级到v2.5.0
        resources:
          requests:
            cpu: "2"    # 从0.5增加到2
            memory: 4Gi  # 从1Gi增加到4Gi
          limits:
            cpu: "4"     # 从1增加到4
            memory: 8Gi  # 从2Gi增加到8Gi
"""

# 测试用例2：数据库配置变更（中风险）
db_change_diff = """
resource "aws_db_instance" "main_database" {
  identifier           = "production-db"
  engine               = "mysql"
  engine_version       = "8.0.32"  # 从5.7升级到8.0
  instance_class       = "db.r6g.2xlarge"  # 从db.r6g.xlarge升级
  allocated_storage    = 500  # 从200GB增加到500GB
  storage_type         = "gp3"  # 从gp2变更到gp3
  max_allocated_storage = 1000
  name                 = "maindb"
  username             = "admin"
  password             = var.db_password
  parameter_group_name = aws_db_parameter_group.main.name
  backup_retention_period = 14
  backup_window        = "03:00-05:00"
  maintenance_window   = "sun:05:00-sun:07:00"
  multi_az             = true
}
"""

# 测试用例3：安全组规则变更（高风险）
sg_rules_diff = """
{
  "SecurityGroupId": "sg-01234567890abcdef",
  "GroupName": "app-server-sg",
  "Description": "Security group for application servers",
  "IpPermissions": [
    {
      "IpProtocol": "tcp",
      "FromPort": 22,
      "ToPort": 22,
      "IpRanges": [
        {
          "CidrIp": "0.0.0.0/0",  // 原为公司IP 10.0.0.0/16，现改为全网开放
          "Description": "SSH access"
        }
      ]
    },
    {
      "IpProtocol": "tcp",
      "FromPort": 3306,
      "ToPort": 3306,  // 新开放MySQL端口
      "IpRanges": [
        {
          "CidrIp": "0.0.0.0/0",  // 对全网开放数据库端口
          "Description": "MySQL access"
        }
      ]
    }
  ]
}
"""

# 调用AI推理服务
def call_ai_service(diff_content):
    response = requests.post("http://localhost:8001/predict", json={"diff": diff_content})
    return response.json()

# 调用LIME解释服务
def call_lime_service(diff_content):
    response = requests.post("http://localhost:8002/explain", json={"diff": diff_content})
    return response.json()

# 测试函数
def test_cloud_changes():
    # 测试Kubernetes部署变更
    print("\n=== Kubernetes部署变更测试 ===")
    k8s_result = call_ai_service(k8s_deployment_diff)
    print("AI推理服务结果:")
    print(json.dumps(k8s_result, indent=2, ensure_ascii=False))
    k8s_explanation = call_lime_service(k8s_deployment_diff)
    print("LIME解释服务结果:")
    print(json.dumps(k8s_explanation, indent=2, ensure_ascii=False))
    
    # 测试数据库配置变更
    print("\n=== 数据库配置变更测试 ===")
    db_result = call_ai_service(db_change_diff)
    print("AI推理服务结果:")
    print(json.dumps(db_result, indent=2, ensure_ascii=False))
    db_explanation = call_lime_service(db_change_diff)
    print("LIME解释服务结果:")
    print(json.dumps(db_explanation, indent=2, ensure_ascii=False))
    
    # 测试安全组规则变更
    print("\n=== 安全组规则变更测试 ===")
    sg_result = call_ai_service(sg_rules_diff)
    print("AI推理服务结果:")
    print(json.dumps(sg_result, indent=2, ensure_ascii=False))
    sg_explanation = call_lime_service(sg_rules_diff)
    print("LIME解释服务结果:")
    print(json.dumps(sg_explanation, indent=2, ensure_ascii=False))

# 验证结果的辅助函数
def verify_results(test_name, result, expected_risk_level):
    print(f"\n验证 {test_name} 结果:")
    if "risk_level" in result and result["risk_level"] == expected_risk_level:
        print(f"✅ 风险等级符合预期: {expected_risk_level}")
    else:
        print(f"❌ 风险等级不符合预期: 预期 {expected_risk_level}, 实际 {result.get('risk_level', '未知')}")
    
    if "description" in result and len(result["description"]) > 0:
        print("✅ 包含风险描述")
    else:
        print("❌ 缺少风险描述")
    
    if "suggestions" in result and len(result["suggestions"]) > 0:
        print("✅ 包含改进建议")
    else:
        print("❌ 缺少改进建议")

# 主函数
def main():
    print("开始云资源变更风险评估测试...")
    test_cloud_changes()
    
    # 等待1秒，确保数据写入完成
    time.sleep(1)
    
    # 获取并验证结果
    k8s_result = call_ai_service(k8s_deployment_diff)
    db_result = call_ai_service(db_change_diff)
    sg_result = call_ai_service(sg_rules_diff)
    
    verify_results("Kubernetes部署变更", k8s_result, "高风险")
    verify_results("数据库配置变更", db_result, "中风险")
    verify_results("安全组规则变更", sg_result, "高风险")
    
    print("\n测试完成!")

if __name__ == "__main__":
    main()