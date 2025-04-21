-- 用户模块表
CREATE TABLE IF NOT EXISTS `user_levels` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '等级ID',
  `name` varchar(50) NOT NULL COMMENT '等级名称',
  `min_points` int(11) UNSIGNED NOT NULL DEFAULT '0' COMMENT '最小积分',
  `discount` decimal(3,2) DEFAULT '1.00' COMMENT '折扣率',
  `icon` varchar(255) DEFAULT NULL COMMENT '等级图标',
  `description` varchar(255) DEFAULT NULL COMMENT '等级描述',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户等级表';

CREATE TABLE IF NOT EXISTS `user_addresses` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '地址ID',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `name` varchar(50) NOT NULL COMMENT '收货人姓名',
  `phone` varchar(20) NOT NULL COMMENT '收货人电话',
  `province` varchar(50) NOT NULL COMMENT '省份',
  `city` varchar(50) NOT NULL COMMENT '城市',
  `district` varchar(50) NOT NULL COMMENT '区/县',
  `detail` varchar(255) NOT NULL COMMENT '详细地址',
  `postal_code` varchar(20) DEFAULT NULL COMMENT '邮政编码',
  `is_default` tinyint(1) DEFAULT '0' COMMENT '是否默认:0否,1是',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户地址表';

-- 商品模块表
CREATE TABLE IF NOT EXISTS `product_attributes` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '属性ID',
  `name` varchar(50) NOT NULL COMMENT '属性名称',
  `category_id` int(11) UNSIGNED DEFAULT NULL COMMENT '所属分类ID,NULL表示通用属性',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序值',
  `is_filter` tinyint(1) DEFAULT '0' COMMENT '是否可筛选:0否,1是',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品属性表';

-- 订单与支付模块表
CREATE TABLE IF NOT EXISTS `orders` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_no` varchar(32) NOT NULL COMMENT '订单编号',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `total_amount` decimal(10,2) NOT NULL COMMENT '订单总金额',
  `pay_amount` decimal(10,2) NOT NULL COMMENT '实付金额',
  `freight_amount` decimal(10,2) DEFAULT '0.00' COMMENT '运费',
  `discount_amount` decimal(10,2) DEFAULT '0.00' COMMENT '优惠金额',
  `coupon_id` bigint(20) UNSIGNED DEFAULT NULL COMMENT '优惠券ID',
  `payment_type` tinyint(1) DEFAULT NULL COMMENT '支付方式:1微信,2余额',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '订单状态:0待付款,1待发货,2待收货,3已完成,4已取消,5已退款',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
  `delivery_time` datetime DEFAULT NULL COMMENT '发货时间',
  `receive_time` datetime DEFAULT NULL COMMENT '收货时间',
  `finish_time` datetime DEFAULT NULL COMMENT '完成时间',
  `cancel_time` datetime DEFAULT NULL COMMENT '取消时间',
  `cancel_reason` varchar(255) DEFAULT NULL COMMENT '取消原因',
  `delivery_company` varchar(64) DEFAULT NULL COMMENT '物流公司',
  `delivery_no` varchar(64) DEFAULT NULL COMMENT '物流单号',
  `receiver_name` varchar(50) NOT NULL COMMENT '收货人姓名',
  `receiver_phone` varchar(20) NOT NULL COMMENT '收货人电话',
  `receiver_province` varchar(50) NOT NULL COMMENT '省份',
  `receiver_city` varchar(50) NOT NULL COMMENT '城市',
  `receiver_district` varchar(50) NOT NULL COMMENT '区/县',
  `receiver_detail` varchar(255) NOT NULL COMMENT '详细地址',
  `note` varchar(255) DEFAULT NULL COMMENT '订单备注',
  `is_deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除:0否,1是',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 系统与管理模块表
CREATE TABLE IF NOT EXISTS `permissions` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '权限ID',
  `parent_id` int(11) UNSIGNED DEFAULT '0' COMMENT '父级ID',
  `name` varchar(50) NOT NULL COMMENT '权限名称',
  `code` varchar(100) NOT NULL COMMENT '权限编码',
  `type` tinyint(1) NOT NULL COMMENT '类型:1模块,2菜单,3操作',
  `icon` varchar(50) DEFAULT NULL COMMENT '图标',
  `path` varchar(100) DEFAULT NULL COMMENT '路径',
  `component` varchar(100) DEFAULT NULL COMMENT '组件',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序值',
  `is_hidden` tinyint(1) DEFAULT '0' COMMENT '是否隐藏:0否,1是',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code` (`code`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_type` (`type`),
  KEY `idx_sort_order` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限表';

-- 营销与内容模块表
CREATE TABLE IF NOT EXISTS `coupons` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '优惠券ID',
  `name` varchar(100) NOT NULL COMMENT '优惠券名称',
  `type` tinyint(1) NOT NULL COMMENT '类型:1满减,2折扣,3无门槛',
  `value` decimal(10,2) NOT NULL COMMENT '面值/折扣',
  `min_amount` decimal(10,2) DEFAULT '0.00' COMMENT '最低使用金额',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  `total` int(11) DEFAULT NULL COMMENT '发行量,NULL表示不限量',
  `used` int(11) DEFAULT '0' COMMENT '已使用数量',
  `per_limit` int(11) DEFAULT '1' COMMENT '每人限领数量',
  `category_ids` varchar(255) DEFAULT NULL COMMENT '可用分类ID,多个以逗号分隔,NULL表示不限制',
  `product_ids` varchar(255) DEFAULT NULL COMMENT '可用商品ID,多个以逗号分隔,NULL表示不限制',
  `description` varchar(255) DEFAULT NULL COMMENT '使用说明',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0无效,1有效',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_type` (`type`),
  KEY `idx_status` (`status`),
  KEY `idx_start_time` (`start_time`),
  KEY `idx_end_time` (`end_time`)
 