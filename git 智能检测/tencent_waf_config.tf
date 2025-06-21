# 腾讯云 WAF 高风险配置变更 - Terraform 配置
# 风险等级: 高风险
# 变更类型: 基础设施安全配置变更
# 影响范围: 生产环境 Web 应用防护

terraform {
  required_providers {
    tencentcloud = {
      source  = "tencentcloudstack/tencentcloud"
      version = "~> 1.81.0"
    }
  }
}

# 配置腾讯云提供商
provider "tencentcloud" {
  secret_id  = var.secret_id
  secret_key = var.secret_key
  region     = var.region
}

# 变量定义
variable "secret_id" {
  description = "腾讯云 Secret ID"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "腾讯云 Secret Key"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "腾讯云地域"
  type        = string
  default     = "ap-guangzhou"
}

variable "domain_name" {
  description = "需要防护的域名"
  type        = string
  default     = "${PRODUCTION_DOMAIN}"
}

variable "waf_instance_id" {
  description = "WAF 实例 ID"
  type        = string
  default     = "${WAF_INSTANCE_ID}"
}

# WAF 实例配置
resource "tencentcloud_waf_clb_instance" "production_waf" {
  instance_name = "production-waf-instance"
  region        = var.region
  
  # 高风险配置：修改实例规格
  edition = "premium"  # 从基础版升级到高级版
  
  # 域名配置
  domain_pkg_count = 10
  qps_limit        = 10000
  
  # 自动续费配置
  auto_renew_flag = 1
  
  tags = {
    Environment = "production"
    Service     = "web-security"
    Risk        = "high"
    ChangeType  = "waf-upgrade"
  }
}

# WAF 域名配置 - 高风险变更
resource "tencentcloud_waf_clb_domain" "production_domain" {
  instance_id = tencentcloud_waf_clb_instance.production_waf.id
  domain      = var.domain_name
  
  # 高风险配置：修改负载均衡器配置
  load_balancer_set {
    load_balancer_id   = "${CLB_INSTANCE_ID}"
    load_balancer_name = "production-clb"
    listener_id        = "${LISTENER_ID}"
    listener_name      = "https-listener"
    vip                = "${VIP_ADDRESS}"
    vport              = 443
    region             = var.region
    protocol           = "HTTPS"
    zone               = "ap-guangzhou-3"
    numerical_vpc_id   = "${VPC_ID}"
    load_balancer_type = "OPEN"
  }
  
  # 高风险配置：启用流量镜像
  flow_mode = 1  # 镜像模式，可能影响性能
  
  # SSL 配置
  https_rewrite = 1
  https_upstream_port = "443"
  
  # 高风险配置：修改上游服务器
  upstream_scheme = "HTTPS"
  upstream_domain = "${UPSTREAM_DOMAIN}"
  
  # 端口配置
  ports {
    port      = "80"
    protocol  = "HTTP"
    upstream_port = "8080"
    upstream_protocol = "HTTP"
  }
  
  ports {
    port      = "443"
    protocol  = "HTTPS"
    upstream_port = "8443"
    upstream_protocol = "HTTPS"
  }
  
  # 高风险配置：禁用某些安全检查
  is_cdn = 0  # 不使用CDN加速
  
  # 日志配置
  cls {
    status     = 1
    logset_id  = "${LOGSET_ID}"
    topic_id   = "${TOPIC_ID}"
  }
}

# WAF 自定义规则 - 高风险变更
resource "tencentcloud_waf_custom_rule" "emergency_rule" {
  domain      = tencentcloud_waf_clb_domain.production_domain.domain
  rule_name   = "生产环境紧急规则调整"
  priority    = 10
  
  # 高风险配置：修改关键安全规则动作
  rule_action = "log"  # 从拦截改为仅记录日志
  
  # 规则状态 - 高风险：禁用关键安全规则
  status = "0"  # 禁用规则
  
  # 匹配策略
  strategies {
    field        = "URI"
    compare_func = "contain"
    content      = "union select"  # SQL注入特征
    arg          = ""
  }
  
  strategies {
    field        = "URI"
    compare_func = "contain"
    content      = "<script>"  # XSS特征
    arg          = ""
  }
  
  strategies {
    field        = "ARGS"
    compare_func = "contain"
    content      = "../"  # 路径遍历特征
    arg          = ""
  }
}

# IP 访问控制规则 - 高风险变更
resource "tencentcloud_waf_ip_access_control" "production_ip_control" {
  domain      = tencentcloud_waf_clb_domain.production_domain.domain
  
  # 高风险配置：添加可能影响正常用户的IP控制规则
  ip_list = [
    "192.168.0.0/16",  # 内网IP段
    "10.0.0.0/8",      # 内网IP段
    "172.16.0.0/12",   # 内网IP段
    "${OFFICE_IP_RANGE}"  # 办公网IP段
  ]
  
  # 高风险配置：设置为拦截动作
  action_type = 40  # 拦截
  valid_time  = 3600  # 1小时有效期
  
  note = "生产环境IP访问控制 - 紧急变更"
}

# WAF 防护等级配置 - 高风险变更
resource "tencentcloud_waf_protection_mode" "production_protection" {
  domain      = tencentcloud_waf_clb_domain.production_domain.domain
  
  # 高风险配置：降低防护等级
  mode = 0  # 设置为观察模式（最低防护等级）
  
  # Web安全开关配置
  web_security = "on"
  
  # 高风险配置：关闭某些防护功能
  access_control = "off"  # 关闭访问控制
  cc_protection  = "off"  # 关闭CC防护
  
  # API安全配置
  api_protection = "on"
  
  # Bot防护配置 - 高风险：降低Bot防护等级
  bot_protection = "off"  # 关闭Bot防护
}

# WAF 白名单规则 - 高风险变更
resource "tencentcloud_waf_domain_white_rule" "emergency_whitelist" {
  domain = tencentcloud_waf_clb_domain.production_domain.domain
  
  # 高风险配置：添加过于宽泛的白名单规则
  rules {
    id           = 1
    status       = 1  # 启用
    name         = "生产环境紧急白名单"
    rule_action  = "white"
    match_func   = "ipmatch"
    match_content = "0.0.0.0/0"  # 危险：允许所有IP
    priority     = 1  # 最高优先级
  }
  
  rules {
    id           = 2
    status       = 1
    name         = "管理员后台白名单"
    rule_action  = "white"
    match_func   = "contain"
    match_content = "/admin"  # 管理员路径白名单
    priority     = 2
  }
  
  rules {
    id           = 3
    status       = 1
    name         = "API接口白名单"
    rule_action  = "white"
    match_func   = "contain"
    match_content = "/api/"  # API路径白名单
    priority     = 3
  }
}

# 输出信息
output "waf_instance_id" {
  description = "WAF 实例 ID"
  value       = tencentcloud_waf_clb_instance.production_waf.id
}

output "waf_domain_config" {
  description = "WAF 域名配置信息"
  value = {
    domain      = tencentcloud_waf_clb_domain.production_domain.domain
    instance_id = tencentcloud_waf_clb_domain.production_domain.instance_id
    flow_mode   = tencentcloud_waf_clb_domain.production_domain.flow_mode
  }
}

output "security_risk_summary" {
  description = "安全风险变更汇总"
  value = {
    risk_level = "HIGH"
    changes = [
      "WAF实例规格升级",
      "防护等级降低至观察模式",
      "添加全网IP白名单规则",
      "禁用关键安全检测规则",
      "关闭CC防护和Bot防护",
      "修改负载均衡器配置"
    ]
    impact = "可能导致Web应用安全防护能力下降"
    recommendation = "建议在变更后立即进行安全测试和监控"
  }
}

# 本地文件输出变更记录
resource "local_file" "change_log" {
  filename = "${path.module}/waf_terraform_change_log.json"
  content = jsonencode({
    timestamp = timestamp()
    change_type = "terraform_waf_config"
    risk_level = "HIGH"
    domain = var.domain_name
    changes = [
      {
        resource = "tencentcloud_waf_clb_instance.production_waf"
        action = "create/update"
        description = "WAF实例配置变更"
        risk = "MEDIUM"
      },
      {
        resource = "tencentcloud_waf_protection_mode.production_protection"
        action = "update"
        description = "防护模式降级为观察模式"
        risk = "HIGH"
      },
      {
        resource = "tencentcloud_waf_domain_white_rule.emergency_whitelist"
        action = "create"
        description = "添加全网IP白名单规则"
        risk = "CRITICAL"
      },
      {
        resource = "tencentcloud_waf_custom_rule.emergency_rule"
        action = "update"
        description = "禁用关键安全检测规则"
        risk = "CRITICAL"
      }
    ]
    total_high_risk_changes = 4
    requires_approval = true
    rollback_plan = "terraform destroy 或 terraform apply 回滚配置"
  })
}