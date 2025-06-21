# 高风险数据库配置变更测试
# 此配置包含多个高风险操作：开放数据库访问、弱密码策略等

# RDS 数据库实例配置 - 高风险设置
resource "alicloud_db_instance" "high_risk_db" {
  engine               = "MySQL"
  engine_version       = "8.0"
  instance_type        = "rds.mysql.s2.large"
  instance_storage     = "20"
  instance_name        = "high-risk-production-db"
  
  # 高风险：允许公网访问
  security_ips = ["0.0.0.0/0"]
  
  # 高风险：弱密码
  master_username = "admin"
  master_password = "123456"
  
  # 高风险：禁用备份
  backup_retention_period = 0
  
  # 高风险：禁用SSL
  ssl_enabled = false
  
  # 高风险：禁用日志
  log_backup = false
  
  tags = {
    Environment = "production"
    Risk        = "high"
    Database    = "mysql"
  }
}

# 数据库账号 - 超级权限
resource "alicloud_db_account" "super_admin" {
  db_instance_id   = alicloud_db_instance.high_risk_db.id
  account_name     = "superadmin"
  account_password = "password123"  # 高风险：弱密码
  account_type     = "Super"        # 高风险：超级管理员权限
}

# 数据库权限 - 开放所有权限
resource "alicloud_db_account_privilege" "super_privilege" {
  instance_id  = alicloud_db_instance.high_risk_db.id
  account_name = alicloud_db_account.super_admin.account_name
  privilege    = "ReadWrite"  # 高风险：读写权限
  db_names     = ["*"]        # 高风险：所有数据库
}

# 数据库连接配置 - 高风险设置
resource "alicloud_db_connection" "public_connection" {
  instance_id       = alicloud_db_instance.high_risk_db.id
  connection_prefix = "public-db"
  port              = "3306"  # 高风险：默认端口
}

# 安全组规则 - 开放数据库端口
resource "alicloud_security_group_rule" "allow_mysql" {
  type              = "ingress"
  ip_protocol       = "tcp"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "3306/3306"   # 高风险：MySQL端口
  priority          = 1
  security_group_id = "sg-xxxxxxxxx"
  cidr_ip           = "0.0.0.0/0"   # 高风险：所有IP可访问
}

# 数据库参数组 - 不安全配置
resource "alicloud_db_parameter_group" "unsafe_params" {
  engine         = "mysql"
  engine_version = "8.0"
  param_detail {
    param_name  = "general_log"      # 高风险：启用通用日志
    param_value = "ON"
  }
  param_detail {
    param_name  = "slow_query_log"   # 高风险：启用慢查询日志
    param_value = "ON"
  }
  param_detail {
    param_name  = "log_queries_not_using_indexes"  # 高风险：记录未使用索引的查询
    param_value = "ON"
  }
}