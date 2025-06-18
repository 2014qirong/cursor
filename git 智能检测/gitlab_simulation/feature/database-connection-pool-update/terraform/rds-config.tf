# RDS 数据库实例配置
resource "aws_db_instance" "risk_assessment_db" {
  identifier = "risk-assessment-mysql"
  
  # 数据库引擎配置
  engine         = "mysql"
  engine_version = "8.0.35"
  instance_class = "db.t3.medium"
  
  # 存储配置
  allocated_storage     = 100
  max_allocated_storage = 500
  storage_type         = "gp2"
  storage_encrypted    = true
  
  # 数据库配置
  db_name  = "risk_assessment_db"
  username = "admin"
  password = var.db_password
  
  # 网络配置
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  
  # 连接配置优化
  parameter_group_name = aws_db_parameter_group.mysql_params.name
  
  # 备份配置
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  # 监控配置
  monitoring_interval = 60
  monitoring_role_arn = aws_iam_role.rds_monitoring_role.arn
  
  # 性能洞察
  performance_insights_enabled = true
  performance_insights_retention_period = 7
  
  tags = {
    Name        = "risk-assessment-db"
    Environment = "production"
    Team        = "database"
  }
}

# 数据库参数组 - 优化连接池相关参数
resource "aws_db_parameter_group" "mysql_params" {
  family = "mysql8.0"
  name   = "risk-assessment-mysql-params"
  
  # 连接相关参数优化
  parameter {
    name  = "max_connections"
    value = "500"  # 从默认151增加到500
  }
  
  parameter {
    name  = "wait_timeout"
    value = "600"  # 10分钟超时
  }
  
  parameter {
    name  = "interactive_timeout"
    value = "600"
  }
  
  parameter {
    name  = "connect_timeout"
    value = "20"   # 连接超时20秒
  }
  
  # 性能优化参数
  parameter {
    name  = "innodb_buffer_pool_size"
    value = "{DBInstanceClassMemory*3/4}"  # 使用75%内存作为缓冲池
  }
  
  parameter {
    name  = "slow_query_log"
    value = "1"    # 启用慢查询日志
  }
  
  parameter {
    name  = "long_query_time"
    value = "2"    # 2秒以上的查询记录为慢查询
  }
  
  tags = {
    Name = "risk-assessment-mysql-params"
  }
}