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

CREATE TABLE IF NOT EXISTS `product_attribute_values` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '属性值ID',
  `product_id` bigint(20) UNSIGNED NOT NULL COMMENT '商品ID',
  `attribute_id` int(11) UNSIGNED NOT NULL COMMENT '属性ID',
  `value` varchar(255) NOT NULL COMMENT '属性值',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_attribute_id` (`attribute_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品属性值表';

CREATE TABLE IF NOT EXISTS `product_specs` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '规格ID',
  `name` varchar(50) NOT NULL COMMENT '规格名称',
  `category_id` int(11) UNSIGNED DEFAULT NULL COMMENT '所属分类ID,NULL表示通用规格',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序值',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品规格表';

CREATE TABLE IF NOT EXISTS `product_spec_values` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '规格值ID',
  `spec_id` int(11) UNSIGNED NOT NULL COMMENT '规格ID',
  `value` varchar(50) NOT NULL COMMENT '规格值',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序值',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_spec_id` (`spec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品规格值表';

CREATE TABLE IF NOT EXISTS `product_skus` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'SKU ID',
  `product_id` bigint(20) UNSIGNED NOT NULL COMMENT '商品ID',
  `sku_code` varchar(50) DEFAULT NULL COMMENT 'SKU编码',
  `spec_json` json NOT NULL COMMENT '规格JSON,格式:{spec_id:spec_value_id,...}',
  `price` decimal(10,2) NOT NULL COMMENT 'SKU价格',
  `stock` int(11) NOT NULL COMMENT 'SKU库存',
  `sku_image` varchar(255) DEFAULT NULL COMMENT 'SKU图片',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_sku_code` (`sku_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品SKU表';

CREATE TABLE IF NOT EXISTS `product_reviews` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '评价ID',
  `product_id` bigint(20) UNSIGNED NOT NULL COMMENT '商品ID',
  `order_id` bigint(20) UNSIGNED NOT NULL COMMENT '订单ID',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `spec_info` varchar(255) DEFAULT NULL COMMENT '规格信息',
  `rating` tinyint(1) NOT NULL DEFAULT '5' COMMENT '评分:1-5',
  `content` text DEFAULT NULL COMMENT '评价内容',
  `images` varchar(1000) DEFAULT NULL COMMENT '图片URL,多个以逗号分隔',
  `reply` text DEFAULT NULL COMMENT '商家回复',
  `reply_time` datetime DEFAULT NULL COMMENT '回复时间',
  `is_anonymous` tinyint(1) DEFAULT '0' COMMENT '是否匿名:0否,1是',
  `is_visible` tinyint(1) DEFAULT '1' COMMENT '是否显示:0否,1是',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品评价表';

CREATE TABLE IF NOT EXISTS `products_recommend` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '推荐ID',
  `product_id` bigint(20) UNSIGNED NOT NULL COMMENT '商品ID',
  `position` varchar(50) NOT NULL COMMENT '推荐位置:home,category,detail',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序值',
  `start_time` datetime DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_position` (`position`),
  KEY `idx_sort_order` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品推荐表'; 