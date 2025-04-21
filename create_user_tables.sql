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

CREATE TABLE IF NOT EXISTS `user_favorites` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `product_id` bigint(20) UNSIGNED NOT NULL COMMENT '商品ID',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_product` (`user_id`,`product_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户收藏表';

CREATE TABLE IF NOT EXISTS `browse_histories` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '历史ID',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `product_id` bigint(20) UNSIGNED NOT NULL COMMENT '商品ID',
  `browse_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '浏览时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_browse_time` (`browse_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='浏览历史表';

CREATE TABLE IF NOT EXISTS `point_records` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `point` int(11) NOT NULL COMMENT '积分变动值',
  `type` tinyint(1) NOT NULL COMMENT '类型:1获取,2消费',
  `source` varchar(50) NOT NULL COMMENT '来源:订单,签到,活动等',
  `source_id` varchar(50) DEFAULT NULL COMMENT '来源ID',
  `description` varchar(255) DEFAULT NULL COMMENT '描述',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='积分记录表';

CREATE TABLE IF NOT EXISTS `user_feedback` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '反馈ID',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `type` varchar(50) NOT NULL COMMENT '反馈类型',
  `content` text NOT NULL COMMENT '反馈内容',
  `contact` varchar(50) DEFAULT NULL COMMENT '联系方式',
  `images` varchar(1000) DEFAULT NULL COMMENT '图片URL,多个以逗号分隔',
  `status` tinyint(1) DEFAULT '0' COMMENT '状态:0未处理,1已处理',
  `reply` text DEFAULT NULL COMMENT '回复内容',
  `reply_time` datetime DEFAULT NULL COMMENT '回复时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户反馈表'; 