# 高风险 VPC 网络配置变更
# 此配置包含多个高风险操作：扩大 CIDR 范围、开放安全组规则等

# VPC 配置 - 扩大 CIDR 范围
resource "alicloud_vpc" "main_vpc" {
  vpc_name   = "high-risk-vpc"
  cidr_block = "10.0.0.0/8"  # 高风险：极大的 CIDR 范围
  
  tags = {
    Environment = "production"
    Risk        = "high"
    Change      = "cidr-expansion"
  }
}

# 子网配置 - 公网子网
resource "alicloud_vswitch" "public_subnet" {
  vpc_id       = alicloud_vpc.main_vpc.id
  cidr_block   = "10.0.1.0/24"
  zone_id      = "cn-hangzhou-a"
  vswitch_name = "public-subnet"
}

# 路由表配置 - 默认路由指向公网网关
resource "alicloud_route_entry" "default_route" {
  route_table_id        = alicloud_vpc.main_vpc.route_table_id
  destination_cidrblock = "0.0.0.0/0"  # 高风险：所有流量
  nexthop_type          = "Instance"
  nexthop_id            = alicloud_instance.nat_gateway.id
}

# 安全组配置 - 开放所有端口
resource "alicloud_security_group" "open_sg" {
  name        = "open-security-group"
  description = "High-risk security group with open access"
  vpc_id      = alicloud_vpc.main_vpc.id
}

# 安全组规则 - 允许所有入站流量
resource "alicloud_security_group_rule" "allow_all_inbound" {
  type              = "ingress"
  ip_protocol       = "all"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "1/65535"     # 高风险：所有端口
  priority          = 1
  security_group_id = alicloud_security_group.open_sg.id
  cidr_ip           = "0.0.0.0/0"   # 高风险：所有 IP
}

# 安全组规则 - 允许所有出站流量
resource "alicloud_security_group_rule" "allow_all_outbound" {
  type              = "egress"
  ip_protocol       = "all"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "1/65535"     # 高风险：所有端口
  priority          = 1
  security_group_id = alicloud_security_group.open_sg.id
  cidr_ip           = "0.0.0.0/0"   # 高风险：所有 IP
}

# NAT 网关实例（用于路由）
resource "alicloud_instance" "nat_gateway" {
  instance_name   = "nat-gateway-instance"
  image_id        = "ubuntu_18_04_64_20G_alibase_20190624.vhd"
  instance_type   = "ecs.t5-lc1m1.small"
  security_groups = [alicloud_security_group.open_sg.id]
  vswitch_id      = alicloud_vswitch.public_subnet.id
  
  tags = {
    Role = "nat-gateway"
    Risk = "high"
  }
}