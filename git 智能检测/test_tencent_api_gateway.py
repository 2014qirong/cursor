#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云原生API网关测试用例生成器
基于腾讯云文档生成各种网关配置变更场景
"""

import requests
import json
import time
import os
import base64
from datetime import datetime
from typing import Dict, List, Any

# 服务配置
AI_INFER_SERVICE_URL = "http://localhost:8001"
GITLAB_WEBHOOK_ENDPOINT = f"{AI_INFER_SERVICE_URL}/gitlab-webhook"
CLB_WEBHOOK_ENDPOINT = f"{AI_INFER_SERVICE_URL}/clb-webhook"

# 腾讯云原生API网关测试用例
api_gateway_test_cases = [
    {
        "name": "高风险 - API网关Kong版本升级",
        "webhook_type": "gitlab",
        "data": {
            "object_kind": "push",
            "event_name": "push",
            "project_id": 201,
            "project": {
                "id": 201,
                "name": "tencent-api-gateway-config",
                "namespace": "infrastructure"
            },
            "commits": [{
                "id": "kong001",
                "message": "Upgrade Kong API Gateway from 2.4.1 to 2.5.1 in production",
                "author": {"name": "DevOps Team"},
                "added": ["terraform/api-gateway-upgrade.tf"],
                "modified": ["config/kong-gateway.yaml", "helm/values-prod.yaml"],
                "removed": ["config/kong-2.4.1-config.yaml"]
            }]
        }
    },
    {
        "name": "高风险 - API网关节点规格扩容",
        "webhook_type": "clb",
        "data": {
            "eventName": "ModifyApiGatewayInstance",
            "eventTime": datetime.now().isoformat(),
            "userIdentity": {
                "type": "Root",
                "principalId": "gateway-admin",
                "arn": "qcs::cam::uin/123456789:root",
                "accountId": "123456789"
            },
            "eventRegion": "ap-beijing",
            "sourceIPAddress": "203.0.113.10",
            "userAgent": "TencentCloud-Console",
            "requestParameters": {
                "gatewayId": "apigw-12345678",
                "instanceType": "kong",
                "nodeSpec": "4C8G",  # 从2C4G升级到4C8G
                "nodeCount": 6,      # 从3个节点扩容到6个节点
                "deploymentMode": "multi-az",
                "enablePublicNetwork": True,
                "bandwidthLimit": 1000  # 带宽从500Mbps提升到1000Mbps
            },
            "responseElements": {
                "requestId": "12345678-1234-1234-1234-123456789012"
            }
        }
    },
    {
        "name": "中风险 - API网关公网负载均衡配置变更",
        "webhook_type": "clb",
        "data": {
            "eventName": "ModifyLoadBalancer",
            "eventTime": datetime.now().isoformat(),
            "userIdentity": {
                "type": "AssumedRole",
                "principalId": "network-engineer",
                "arn": "qcs::cam::uin/123456789:assumed-role/NetworkRole/network-engineer",
                "accountId": "123456789"
            },
            "eventRegion": "ap-shanghai",
            "sourceIPAddress": "10.0.1.100",
            "userAgent": "TencentCloud-SDK",
            "requestParameters": {
                "loadBalancerId": "lb-apigw-12345",
                "loadBalancerType": "OPEN",  # 公网负载均衡
                "chargeType": "TRAFFIC_POSTPAID_BY_HOUR",  # 按流量计费
                "internetMaxBandwidthOut": 2048,  # 带宽上限2048Mbps
                "masterZoneId": "ap-shanghai-1",
                "slaveZoneId": "ap-shanghai-2",  # 多可用区配置
                "projectId": 0
            },
            "responseElements": {
                "requestId": "87654321-4321-4321-4321-210987654321"
            }
        }
    },
    {
        "name": "中风险 - API网关CLS日志服务配置",
        "webhook_type": "gitlab",
        "data": {
            "object_kind": "push",
            "event_name": "push",
            "project_id": 202,
            "project": {
                "id": 202,
                "name": "api-gateway-logging",
                "namespace": "monitoring"
            },
            "commits": [{
                "id": "cls001",
                "message": "Enable CLS log service for API Gateway with custom log format",
                "author": {"name": "SRE Team"},
                "added": ["logging/cls-logset.yaml", "logging/cls-topic.yaml"],
                "modified": ["config/gateway-logging.yaml", "terraform/cls-config.tf"],
                "removed": []
            }]
        }
    },
    {
        "name": "高风险 - API网关VPC网络配置变更",
        "webhook_type": "clb",
        "data": {
            "eventName": "ModifyVpcAttribute",
            "eventTime": datetime.now().isoformat(),
            "userIdentity": {
                "type": "Root",
                "principalId": "vpc-admin",
                "arn": "qcs::cam::uin/123456789:root",
                "accountId": "123456789"
            },
            "eventRegion": "ap-guangzhou",
            "sourceIPAddress": "172.16.0.10",
            "userAgent": "TencentCloud-Terraform",
            "requestParameters": {
                "vpcId": "vpc-apigw-12345",
                "vpcName": "api-gateway-vpc-prod",
                "cidrBlock": "10.0.0.0/16",  # VPC CIDR变更
                "subnetId": "subnet-apigw-001",
                "subnetCidr": "10.0.1.0/24",  # 子网CIDR变更
                "gatewayId": "apigw-12345678",
                "enableDnsHostnames": True,
                "enableDnsResolution": True
            },
            "responseElements": {
                "requestId": "vpc12345-1234-1234-1234-123456789012"
            }
        }
    },
    {
        "name": "低风险 - API网关标签管理",
        "webhook_type": "gitlab",
        "data": {
            "object_kind": "push",
            "event_name": "push",
            "project_id": 203,
            "project": {
                "id": 203,
                "name": "api-gateway-tags",
                "namespace": "management"
            },
            "commits": [{
                "id": "tag001",
                "message": "Update API Gateway resource tags for better cost management",
                "author": {"name": "FinOps Team"},
                "added": ["tags/cost-allocation.yaml"],
                "modified": ["terraform/tags.tf", "config/resource-tags.yaml"],
                "removed": ["tags/deprecated-tags.yaml"]
            }]
        }
    },
    {
        "name": "高风险 - API网关授权角色配置",
        "webhook_type": "clb",
        "data": {
            "eventName": "AttachRolePolicy",
            "eventTime": datetime.now().isoformat(),
            "userIdentity": {
                "type": "Root",
                "principalId": "security-admin",
                "arn": "qcs::cam::uin/123456789:root",
                "accountId": "123456789"
            },
            "eventRegion": "ap-beijing",
            "sourceIPAddress": "203.0.113.20",
            "userAgent": "TencentCloud-Console",
            "requestParameters": {
                "roleName": "ApiGateWay_QCSRole",
                "policyName": "QcloudAccessForApiGateWayRoleInCloudNativeAPIGateway",
                "policyDocument": {
                    "version": "2.0",
                    "statement": [{
                        "effect": "allow",
                        "action": [
                            "cls:*",
                            "vpc:*",
                            "clb:*",
                            "monitor:*"
                        ],
                        "resource": "*"
                    }]
                }
            },
            "responseElements": {
                "requestId": "role12345-1234-1234-1234-123456789012"
            }
        }
    }
]

def test_webhook(webhook_type, data, test_name):
    """测试Webhook端点"""
    if webhook_type == "gitlab":
        endpoint = GITLAB_WEBHOOK_ENDPOINT
    elif webhook_type == "clb":
        endpoint = CLB_WEBHOOK_ENDPOINT
    else:
        print(f"❌ 未知的webhook类型: {webhook_type}")
        return False
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(endpoint, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {test_name} - 成功")
            print(f"   风险等级: {result.get('risk_level', 'N/A')}")
            print(f"   风险概率: {result.get('risk_probability', 'N/A')}")
            print(f"   响应时间: {response.elapsed.total_seconds():.2f}s")
            return True
        else:
            print(f"❌ {test_name} - 失败 (HTTP {response.status_code})")
            print(f"   错误信息: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {test_name} - 网络错误: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ {test_name} - 未知错误: {str(e)}")
        return False

def run_api_gateway_tests():
    """运行所有腾讯云API网关测试用例"""
    print("🚀 开始腾讯云原生API网关测试用例")
    print("=" * 60)
    
    success_count = 0
    total_count = len(api_gateway_test_cases)
    
    for i, test_case in enumerate(api_gateway_test_cases, 1):
        print(f"\n[{i}/{total_count}] 测试: {test_case['name']}")
        print("-" * 40)
        
        success = test_webhook(
            test_case['webhook_type'],
            test_case['data'],
            test_case['name']
        )
        
        if success:
            success_count += 1
        
        # 测试间隔
        if i < total_count:
            time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"📊 测试完成: {success_count}/{total_count} 成功")
    print(f"📈 成功率: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 所有腾讯云API网关测试用例通过!")
    else:
        print(f"⚠️  有 {total_count - success_count} 个测试用例失败，请检查服务状态")

def _generate_plugin_config_change() -> Dict[str, Any]:
    """生成插件配置变更测试用例"""
    return {
        "test_name": "API网关插件配置变更",
        "risk_level": "medium",
        "description": "修改Kong网关插件配置，可能影响API访问控制",
        "files_changed": [
            "config/kong-plugins.yaml"
        ],
        "diff_content": """
--- a/config/kong-plugins.yaml
+++ b/config/kong-plugins.yaml
@@ -15,7 +15,7 @@ plugins:
  - name: rate-limiting
    config:
-      minute: 1000
+      minute: 500
      hour: 10000
      day: 100000
      policy: redis
@@ -45,6 +45,12 @@ plugins:
      anonymous: null
      run_on_preflight: true
    tags:
      - auth
      - jwt
+  - name: ip-restriction
+    config:
+      allow:
+        - 10.0.0.0/8
+      deny:
+        - 192.168.1.100
        """,
        "commit_message": "feat: 调整API网关限流策略和IP访问控制",
        "author": "devops-team",
        "branch": "feature/gateway-security-update"
    }

def _generate_high_risk_production_change() -> Dict[str, Any]:
    """生成高风险生产环境变更测试用例"""
    return {
        "test_name": "生产环境API网关核心配置变更",
        "risk_level": "high",
        "description": "修改生产环境API网关核心配置，包括负载均衡和安全策略",
        "files_changed": [
            "terraform/production/tencent_api_gateway.tf",
            "k8s/production/tencent-api-gateway-deployment.yaml"
        ],
        "diff_content": """
--- a/terraform/production/tencent_api_gateway.tf
+++ b/terraform/production/tencent_api_gateway.tf
@@ -25,7 +25,7 @@ variable "node_count" {
  description = "网关节点数量"
  type        = number
-  default     = 3
+  default     = 1
}

variable "node_spec" {
@@ -45,7 +45,7 @@ resource "tencentcloud_vpc" "api_gateway_vpc" {
  name       = "${var.gateway_name}-vpc"
-  cidr_block = "10.0.0.0/16"
+  cidr_block = "172.16.0.0/12"
  
  tags = {
    Name        = "${var.gateway_name}-vpc"
--- a/k8s/production/tencent-api-gateway-deployment.yaml
+++ b/k8s/production/tencent-api-gateway-deployment.yaml
@@ -180,7 +180,7 @@ metadata:
  labels:
    app: kong
spec:
-  replicas: 3
+  replicas: 1
  strategy:
    type: RollingUpdate
    rollingUpdate:
@@ -220,8 +220,8 @@ spec:
        resources:
          requests:
-            memory: "512Mi"
-            cpu: "250m"
+            memory: "128Mi"
+            cpu: "100m"
          limits:
-            memory: "1Gi"
-            cpu: "500m"
+            memory: "256Mi"
+            cpu: "200m"
        """,
        "commit_message": "URGENT: 紧急调整生产环境API网关资源配置",
        "author": "ops-emergency",
        "branch": "hotfix/production-gateway-scaling"
    }

def _generate_database_config_change() -> Dict[str, Any]:
    """生成数据库配置变更测试用例"""
    return {
        "test_name": "API网关数据库配置变更",
        "risk_level": "high",
        "description": "修改API网关后端数据库配置，可能导致服务中断",
        "files_changed": [
            "k8s/tencent-api-gateway-deployment.yaml",
            "config/database-config.yaml"
        ],
        "diff_content": """
--- a/k8s/tencent-api-gateway-deployment.yaml
+++ b/k8s/tencent-api-gateway-deployment.yaml
@@ -85,7 +85,7 @@ spec:
        - name: POSTGRES_DB
          value: kong
        - name: POSTGRES_USER
-          value: kong
+          value: kong_admin
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
@@ -125,7 +125,7 @@ spec:
        - name: KONG_PG_HOST
-          value: postgres-service.api-gateway.svc.cluster.local
+          value: postgres-cluster.database.svc.cluster.local
        - name: KONG_PG_PORT
          value: "5432"
        - name: KONG_PG_DATABASE
--- a/config/database-config.yaml
+++ b/config/database-config.yaml
@@ -5,7 +5,7 @@ database:
  type: postgresql
  host: postgres-service.api-gateway.svc.cluster.local
  port: 5432
-  database: kong
+  database: kong_production
  username: kong
  password: ${POSTGRES_PASSWORD}
  pool_size: 20
-  max_connections: 100
+  max_connections: 200
  ssl_mode: require
        """,
        "commit_message": "feat: 升级API网关数据库配置以支持高并发",
        "author": "database-team",
        "branch": "feature/database-optimization"
    }

def _generate_secret_management_change() -> Dict[str, Any]:
    """生成密钥管理变更测试用例"""
    return {
        "test_name": "API网关密钥和证书管理变更",
        "risk_level": "critical",
        "description": "修改API网关的JWT密钥和SSL证书配置，高度敏感",
        "files_changed": [
            "config/api-gateway-config.yaml",
            "k8s/secrets.yaml",
            "terraform/tencent_api_gateway.tf"
        ],
        "diff_content": """
--- a/config/api-gateway-config.yaml
+++ b/config/api-gateway-config.yaml
@@ -425,7 +425,7 @@ consumers:
    jwt_secrets:
      - key: mobile-app-issuer
-        secret: "mobile-app-jwt-secret-key-2023"
+        secret: "mobile-app-jwt-secret-key-2024-updated"
        algorithm: HS256
    
  - username: web-app
@@ -436,7 +436,7 @@ consumers:
    jwt_secrets:
      - key: web-app-issuer
-        secret: "web-app-jwt-secret-key-2023"
+        secret: "web-app-jwt-secret-key-2024-updated"
        algorithm: HS256
--- a/k8s/secrets.yaml
+++ b/k8s/secrets.yaml
@@ -8,8 +8,8 @@ metadata:
type: Opaque
data:
  # base64编码的密码
-  postgres-password: a29uZ19wYXNzd29yZA==
-  postgres-user: a29uZw==
+  postgres-password: bmV3X3Bvc3RncmVzX3Bhc3N3b3JkXzIwMjQ=
+  postgres-user: a29uZ19hZG1pbg==
--- a/terraform/tencent_api_gateway.tf
+++ b/terraform/tencent_api_gateway.tf
@@ -180,7 +180,7 @@ resource "tencentcloud_clb_listener" "api_gateway_https" {
  port          = 443
  protocol      = "HTTPS"
  certificate_ssl_mode = "UNIDIRECTIONAL"
-  certificate_id = var.ssl_certificate_id
+  certificate_id = "cert-new-2024-production"
  
  health_check_switch = true
        """,
        "commit_message": "SECURITY: 更新API网关所有密钥和证书配置",
        "author": "security-team",
        "branch": "security/credential-rotation-2024"
    }

if __name__ == "__main__":
    run_api_gateway_tests()