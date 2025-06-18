# 腾讯云原生API网关 Terraform 配置
# 基于腾讯云文档的网关配置示例

terraform {
  required_providers {
    tencentcloud = {
      source  = "tencentcloudstack/tencentcloud"
      version = "~> 1.81.0"
    }
  }
}

# 配置腾讯云Provider
provider "tencentcloud" {
  region = var.region
}

# 变量定义
variable "region" {
  description = "腾讯云地域"
  type        = string
  default     = "ap-beijing"
}

variable "availability_zones" {
  description = "可用区列表"
  type        = list(string)
  default     = ["ap-beijing-1", "ap-beijing-2", "ap-beijing-3"]
}

variable "gateway_name" {
  description = "API网关名称"
  type        = string
  default     = "prod-api-gateway"
}

variable "node_count" {
  description = "网关节点数量"
  type        = number
  default     = 3
}

variable "node_spec" {
  description = "节点规格"
  type        = string
  default     = "2C4G"
}

variable "kong_version" {
  description = "Kong版本"
  type        = string
  default     = "2.5.1"
}

# VPC网络配置
resource "tencentcloud_vpc" "api_gateway_vpc" {
  name       = "${var.gateway_name}-vpc"
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name        = "${var.gateway_name}-vpc"
    Environment = "production"
    Service     = "api-gateway"
    ManagedBy   = "terraform"
  }
}

# 子网配置
resource "tencentcloud_subnet" "api_gateway_subnet" {
  count             = length(var.availability_zones)
  name              = "${var.gateway_name}-subnet-${count.index + 1}"
  vpc_id            = tencentcloud_vpc.api_gateway_vpc.id
  availability_zone = var.availability_zones[count.index]
  cidr_block        = "10.0.${count.index + 1}.0/24"
  is_multicast      = false
  
  tags = {
    Name        = "${var.gateway_name}-subnet-${count.index + 1}"
    Environment = "production"
    Service     = "api-gateway"
    AZ          = var.availability_zones[count.index]
  }
}

# 安全组配置
resource "tencentcloud_security_group" "api_gateway_sg" {
  name        = "${var.gateway_name}-sg"
  description = "Security group for API Gateway"
  
  tags = {
    Name        = "${var.gateway_name}-sg"
    Environment = "production"
    Service     = "api-gateway"
  }
}

# 安全组规则 - 入站
resource "tencentcloud_security_group_lite_rule" "api_gateway_ingress" {
  security_group_id = tencentcloud_security_group.api_gateway_sg.id
  
  ingress = [
    "ACCEPT#0.0.0.0/0#80#TCP",
    "ACCEPT#0.0.0.0/0#443#TCP",
    "ACCEPT#10.0.0.0/16#8000#TCP",
    "ACCEPT#10.0.0.0/16#8001#TCP",
    "ACCEPT#10.0.0.0/16#8443#TCP",
    "ACCEPT#10.0.0.0/16#8444#TCP"
  ]
  
  egress = [
    "ACCEPT#0.0.0.0/0#ALL#ALL"
  ]
}

# CLB负载均衡器配置
resource "tencentcloud_clb_instance" "api_gateway_clb" {
  network_type              = "OPEN"  # 公网负载均衡
  clb_name                 = "${var.gateway_name}-clb"
  project_id               = 0
  vpc_id                   = tencentcloud_vpc.api_gateway_vpc.id
  subnet_id                = tencentcloud_subnet.api_gateway_subnet[0].id
  load_balancer_pass_to_target = true
  
  # 多可用区配置
  master_zone_id = var.availability_zones[0]
  slave_zone_id  = var.availability_zones[1]
  
  # 带宽配置
  internet_charge_type       = "TRAFFIC_POSTPAID_BY_HOUR"
  internet_max_bandwidth_out = 1000
  
  security_groups = [tencentcloud_security_group.api_gateway_sg.id]
  
  tags = {
    Name        = "${var.gateway_name}-clb"
    Environment = "production"
    Service     = "api-gateway"
    ChargeType  = "traffic"
  }
}

# CLB监听器配置
resource "tencentcloud_clb_listener" "api_gateway_http" {
  clb_id        = tencentcloud_clb_instance.api_gateway_clb.id
  listener_name = "${var.gateway_name}-http"
  port          = 80
  protocol      = "HTTP"
  
  health_check_switch = true
  health_check_time_out = 5
  health_check_interval_time = 10
  health_check_health_num = 3
  health_check_unhealth_num = 3
  health_check_http_code = 200
  health_check_http_path = "/health"
  health_check_http_method = "GET"
}

resource "tencentcloud_clb_listener" "api_gateway_https" {
  clb_id        = tencentcloud_clb_instance.api_gateway_clb.id
  listener_name = "${var.gateway_name}-https"
  port          = 443
  protocol      = "HTTPS"
  certificate_ssl_mode = "UNIDIRECTIONAL"
  certificate_id = var.ssl_certificate_id
  
  health_check_switch = true
  health_check_time_out = 5
  health_check_interval_time = 10
  health_check_health_num = 3
  health_check_unhealth_num = 3
  health_check_http_code = 200
  health_check_http_path = "/health"
  health_check_http_method = "GET"
}

# CLS日志集配置
resource "tencentcloud_cls_logset" "api_gateway_logset" {
  logset_name = "${var.gateway_name}-logs"
  period      = 30  # 日志保存30天
  
  tags = {
    Name        = "${var.gateway_name}-logs"
    Environment = "production"
    Service     = "api-gateway"
  }
}

# CLS日志主题配置
resource "tencentcloud_cls_topic" "api_gateway_access_log" {
  topic_name           = "${var.gateway_name}-access-log"
  logset_id           = tencentcloud_cls_logset.api_gateway_logset.id
  auto_split          = true
  max_split_partitions = 20
  partition_count     = 1
  period              = 30
  storage_type        = "hot"
  
  tags = {
    Name        = "${var.gateway_name}-access-log"
    Environment = "production"
    Service     = "api-gateway"
    LogType     = "access"
  }
}

resource "tencentcloud_cls_topic" "api_gateway_error_log" {
  topic_name           = "${var.gateway_name}-error-log"
  logset_id           = tencentcloud_cls_logset.api_gateway_logset.id
  auto_split          = true
  max_split_partitions = 20
  partition_count     = 1
  period              = 30
  storage_type        = "hot"
  
  tags = {
    Name        = "${var.gateway_name}-error-log"
    Environment = "production"
    Service     = "api-gateway"
    LogType     = "error"
  }
}

# CAM角色配置
resource "tencentcloud_cam_role" "api_gateway_role" {
  name     = "ApiGateWay_QCSRole"
  document = jsonencode({
    version = "2.0"
    statement = [{
      action = "name/sts:AssumeRole"
      effect = "allow"
      principal = {
        service = ["apigateway.qcloud.com"]
      }
    }]
  })
  description = "API Gateway service role"
  
  tags = {
    Name        = "ApiGateWay_QCSRole"
    Environment = "production"
    Service     = "api-gateway"
  }
}

# CAM策略配置
resource "tencentcloud_cam_policy" "api_gateway_policy" {
  name     = "QcloudAccessForApiGateWayRoleInCloudNativeAPIGateway"
  document = jsonencode({
    version = "2.0"
    statement = [
      {
        effect = "allow"
        action = [
          "cls:*",
          "vpc:Describe*",
          "vpc:CreateNetworkInterface",
          "vpc:AttachNetworkInterface",
          "vpc:DetachNetworkInterface",
          "vpc:DeleteNetworkInterface",
          "clb:*",
          "monitor:*",
          "tag:*"
        ]
        resource = "*"
      }
    ]
  })
  description = "Policy for API Gateway to access other Tencent Cloud services"
}

# 角色策略绑定
resource "tencentcloud_cam_role_policy_attachment" "api_gateway_policy_attachment" {
  role_name   = tencentcloud_cam_role.api_gateway_role.name
  policy_name = tencentcloud_cam_policy.api_gateway_policy.name
}

# 输出配置
output "vpc_id" {
  description = "VPC ID"
  value       = tencentcloud_vpc.api_gateway_vpc.id
}

output "subnet_ids" {
  description = "Subnet IDs"
  value       = tencentcloud_subnet.api_gateway_subnet[*].id
}

output "security_group_id" {
  description = "Security Group ID"
  value       = tencentcloud_security_group.api_gateway_sg.id
}

output "clb_id" {
  description = "CLB Instance ID"
  value       = tencentcloud_clb_instance.api_gateway_clb.id
}

output "clb_vip" {
  description = "CLB VIP Address"
  value       = tencentcloud_clb_instance.api_gateway_clb.clb_vips
}

output "logset_id" {
  description = "CLS Logset ID"
  value       = tencentcloud_cls_logset.api_gateway_logset.id
}

output "access_log_topic_id" {
  description = "Access Log Topic ID"
  value       = tencentcloud_cls_topic.api_gateway_access_log.id
}

output "error_log_topic_id" {
  description = "Error Log Topic ID"
  value       = tencentcloud_cls_topic.api_gateway_error_log.id
}

output "api_gateway_role_arn" {
  description = "API Gateway Service Role ARN"
  value       = tencentcloud_cam_role.api_gateway_role.arn
}

# 变量定义文件需要的额外变量
variable "ssl_certificate_id" {
  description = "SSL证书ID"
  type        = string
  default     = ""
}