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

CREATE TABLE IF NOT EXISTS `admin_operation_logs` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `admin_id` int(11) UNSIGNED NOT NULL COMMENT '管理员ID',
  `admin_name` varchar(50) NOT NULL COMMENT '管理员名称',
  `ip` varchar(64) NOT NULL COMMENT 'IP地址',
  `method` varchar(10) NOT NULL COMMENT '请求方法',
  `url` varchar(255) NOT NULL COMMENT '请求URL',
  `params` text DEFAULT NULL COMMENT '请求参数',
  `operation` varchar(255) NOT NULL COMMENT '操作说明',
  `status` tinyint(1) NOT NULL COMMENT '状态:0失败,1成功',
  `error_msg` varchar(255) DEFAULT NULL COMMENT '错误信息',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_admin_id` (`admin_id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员操作日志表';

CREATE TABLE IF NOT EXISTS `system_configs` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `group` varchar(50) NOT NULL COMMENT '配置分组',
  `name` varchar(50) NOT NULL COMMENT '配置名称',
  `key` varchar(50) NOT NULL COMMENT '配置键名',
  `value` text DEFAULT NULL COMMENT '配置值',
  `type` varchar(20) NOT NULL COMMENT '值类型:string,number,boolean,array,object',
  `options` text DEFAULT NULL COMMENT '选项,JSON格式',
  `description` varchar(255) DEFAULT NULL COMMENT '描述',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序值',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_key` (`key`),
  KEY `idx_group` (`group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';

CREATE TABLE IF NOT EXISTS `regions` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '地区ID',
  `parent_id` int(11) UNSIGNED DEFAULT '0' COMMENT '父级ID',
  `name` varchar(50) NOT NULL COMMENT '地区名称',
  `code` varchar(20) DEFAULT NULL COMMENT '地区编码',
  `level` tinyint(1) NOT NULL COMMENT '层级:1省,2市,3区/县',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_level` (`level`),
  KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地区表';

CREATE TABLE IF NOT EXISTS `api_logs` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user_id` bigint(20) UNSIGNED DEFAULT NULL COMMENT '用户ID',
  `ip` varchar(64) NOT NULL COMMENT 'IP地址',
  `method` varchar(10) NOT NULL COMMENT '请求方法',
  `uri` varchar(255) NOT NULL COMMENT '请求URI',
  `params` text DEFAULT NULL COMMENT '请求参数',
  `response_code` int(11) NOT NULL COMMENT '响应状态码',
  `response_time` int(11) NOT NULL COMMENT '响应时间(ms)',
  `user_agent` varchar(255) DEFAULT NULL COMMENT '用户代理',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_uri` (`uri`(191)),
  KEY `idx_response_code` (`response_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='API调用日志表';

CREATE TABLE IF NOT EXISTS `app_versions` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '版本ID',
  `version` varchar(20) NOT NULL COMMENT '版本号',
  `platform` varchar(20) NOT NULL COMMENT '平台:android,ios',
  `download_url` varchar(255) DEFAULT NULL COMMENT '下载地址',
  `description` text DEFAULT NULL COMMENT '更新说明',
  `is_force` tinyint(1) DEFAULT '0' COMMENT '是否强制更新:0否,1是',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1启用',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_platform` (`platform`),
  KEY `idx_version` (`version`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='应用版本表';

CREATE TABLE IF NOT EXISTS `statistics_daily` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '统计ID',
  `date` date NOT NULL COMMENT '统计日期',
  `new_users` int(11) DEFAULT '0' COMMENT '新增用户数',
  `active_users` int(11) DEFAULT '0' COMMENT '活跃用户数',
  `orders` int(11) DEFAULT '0' COMMENT '订单总数',
  `paid_orders` int(11) DEFAULT '0' COMMENT '已支付订单数',
  `sales_amount` decimal(10,2) DEFAULT '0.00' COMMENT '销售总额',
  `refund_amount` decimal(10,2) DEFAULT '0.00' COMMENT '退款总额',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日统计表'; 