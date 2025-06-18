# RDS MySQL 生产实例配置
resource "aws_db_instance" "mysql_prod" {
  identifier = "rds-mysql-prod-001"
  
  # 实例规格配置
  instance_class    = "db.r5.2xlarge"
  engine           = "mysql"
  engine_version   = "8.0.35"
  allocated_storage = 1000
  max_allocated_storage = 2000
  storage_type     = "gp3"
  storage_encrypted = true
  kms_key_id       = aws_kms_key.rds_key.arn
  
  # 数据库配置
  db_name  = "production_db"
  username = "admin"
  password = var.db_password
  port     = 3306
  
  # 网络配置
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.prod_db_subnet_group.name
  publicly_accessible    = false
  
  # 高可用配置
  multi_az               = true
  availability_zone      = "us-east-1a"
  
  # 备份配置
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  delete_automated_backups = false
  
  # 监控配置
  monitoring_interval = 60
  monitoring_role_arn = aws_iam_role.rds_monitoring_role.arn
  performance_insights_enabled = true
  performance_insights_retention_period = 7
  enabled_cloudwatch_logs_exports = ["error", "general", "slow-query"]
  
  # 参数组配置
  parameter_group_name = aws_db_parameter_group.mysql_prod_params.name
  option_group_name    = aws_db_option_group.mysql_prod_options.name
  
  # 安全配置
  deletion_protection = true
  skip_final_snapshot = false
  final_snapshot_identifier = "rds-mysql-prod-001-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  
  # 自动升级配置
  auto_minor_version_upgrade = false
  allow_major_version_upgrade = false
  
  # IAM数据库认证
  iam_database_authentication_enabled = true
  
  tags = {
    Name            = "MySQL Production Database"
    Environment     = "Production"
    Service         = "MainDatabase"
    CriticalLevel   = "High"
    BackupRequired  = "true"
    ComplianceRequired = "PCI-DSS"
    ManagedBy       = "Terraform"
  }
}

# 数据库参数组
resource "aws_db_parameter_group" "mysql_prod_params" {
  family = "mysql8.0"
  name   = "prod-mysql-params"
  
  parameter {
    name  = "max_connections"
    value = "2000"
  }
  
  parameter {
    name  = "max_user_connections"
    value = "1800"
  }
  
  parameter {
    name  = "connect_timeout"
    value = "30"
  }
  
  parameter {
    name  = "wait_timeout"
    value = "28800"
  }
  
  parameter {
    name  = "interactive_timeout"
    value = "28800"
  }
  
  parameter {
    name  = "innodb_buffer_pool_size"
    value = "{DBInstanceClassMemory*3/4}"
  }
  
  parameter {
    name  = "query_cache_size"
    value = "268435456"  # 256MB
  }
  
  parameter {
    name  = "query_cache_type"
    value = "1"
  }
  
  parameter {
    name  = "slow_query_log"
    value = "1"
  }
  
  parameter {
    name  = "long_query_time"
    value = "2"
  }
  
  parameter {
    name  = "log_queries_not_using_indexes"
    value = "1"
  }
  
  tags = {
    Name        = "MySQL Production Parameters"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# 数据库选项组
resource "aws_db_option_group" "mysql_prod_options" {
  name                 = "prod-mysql-options"
  option_group_description = "MySQL production options"
  engine_name          = "mysql"
  major_engine_version = "8.0"
  
  tags = {
    Name        = "MySQL Production Options"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# 只读副本配置
resource "aws_db_instance" "mysql_prod_read_replica_1" {
  identifier = "rds-mysql-prod-001-read-1"
  replicate_source_db = aws_db_instance.mysql_prod.id
  
  instance_class = "db.r5.xlarge"
  publicly_accessible = false
  availability_zone = "us-east-1b"
  
  monitoring_interval = 60
  monitoring_role_arn = aws_iam_role.rds_monitoring_role.arn
  performance_insights_enabled = true
  
  tags = {
    Name        = "MySQL Production Read Replica 1"
    Environment = "Production"
    Service     = "MainDatabase"
    Role        = "ReadReplica"
    ManagedBy   = "Terraform"
  }
}

resource "aws_db_instance" "mysql_prod_read_replica_2" {
  identifier = "rds-mysql-prod-001-read-2"
  replicate_source_db = aws_db_instance.mysql_prod.id
  
  instance_class = "db.r5.xlarge"
  publicly_accessible = false
  availability_zone = "us-east-1c"
  
  monitoring_interval = 60
  monitoring_role_arn = aws_iam_role.rds_monitoring_role.arn
  performance_insights_enabled = true
  
  tags = {
    Name        = "MySQL Production Read Replica 2"
    Environment = "Production"
    Service     = "MainDatabase"
    Role        = "ReadReplica"
    ManagedBy   = "Terraform"
  }
}