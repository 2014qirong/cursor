provider "aws" {
  region = "ap-southeast-1"
}

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
  skip_final_snapshot  = false
  final_snapshot_identifier = "production-db-final-snapshot"
  deletion_protection  = true
  performance_insights_enabled = true
  enabled_cloudwatch_logs_exports = ["error", "general", "slowquery"]
  
  tags = {
    Name = "MainProductionDB"
    Environment = "production"
  }
}

resource "aws_db_parameter_group" "main" {
  name   = "production-mysql8-params"
  family = "mysql8.0"

  parameter {
    name  = "max_connections"
    value = "1000"  # 从500增加到1000
  }

  parameter {
    name  = "innodb_buffer_pool_size"
    value = "8589934592"  # 从4G增加到8G
  }

  parameter {
    name  = "innodb_log_file_size"
    value = "1073741824"  # 从256M增加到1G
  }

  parameter {
    name  = "slow_query_log"
    value = "1"
  }

  parameter {
    name  = "long_query_time"
    value = "2"  # 从5秒降低到2秒
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "main-db-subnet-group"
  subnet_ids = var.private_subnet_ids
} 