-- 创建商城数据库
CREATE DATABASE IF NOT EXISTS `mall_dev` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 授权
GRANT ALL PRIVILEGES ON mall_dev.* TO 'dev_user'@'%';
FLUSH PRIVILEGES;

-- 使用商城数据库
USE `mall_dev`;

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `openid` varchar(64) NOT NULL COMMENT '微信openid',
  `nickname` varchar(50) DEFAULT NULL COMMENT '用户昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像URL',
  `gender` tinyint(1) DEFAULT '0' COMMENT '性别:0未知,1男,2女',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `points` int(11) UNSIGNED DEFAULT '0' COMMENT '积分',
  `balance` decimal(10,2) DEFAULT '0.00' COMMENT '余额',
  `level_id` int(11) UNSIGNED DEFAULT '1' COMMENT '等级ID',
  `is_disabled` tinyint(1) DEFAULT '0' COMMENT '是否禁用:0否,1是',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(50) DEFAULT NULL COMMENT '最后登录IP',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_openid` (`openid`),
  KEY `idx_phone` (`phone`),
  KEY `idx_level_id` (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 商品分类表
CREATE TABLE IF NOT EXISTS `product_categories` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `parent_id` int(11) UNSIGNED DEFAULT '0' COMMENT '父分类ID,0为一级分类',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `icon` varchar(255) DEFAULT NULL COMMENT '分类图标',
  `banner` varchar(255) DEFAULT NULL COMMENT '分类banner图',
  `sort_order` int(11) DEFAULT '0' COMMENT '排序值,越小越靠前',
  `level` tinyint(1) DEFAULT '1' COMMENT '分类级别',
  `is_visible` tinyint(1) DEFAULT '1' COMMENT '是否显示:0否,1是',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_sort` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- 商品表
CREATE TABLE IF NOT EXISTS `products` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `category_id` int(11) UNSIGNED NOT NULL COMMENT '分类ID',
  `name` varchar(100) NOT NULL COMMENT '商品名称',
  `subtitle` varchar(200) DEFAULT NULL COMMENT '副标题',
  `main_image` varchar(255) NOT NULL COMMENT '主图',
  `sub_images` text DEFAULT NULL COMMENT '子图,JSON格式',
  `detail` text DEFAULT NULL COMMENT '商品详情',
  `price` decimal(10,2) NOT NULL COMMENT '商品价格',
  `stock` int(11) NOT NULL COMMENT '库存',
  `sale` int(11) DEFAULT '0' COMMENT '销量',
  `unit` varchar(20) DEFAULT NULL COMMENT '单位',
  `weight` decimal(10,2) DEFAULT NULL COMMENT '重量,单位g',
  `is_hot` tinyint(1) DEFAULT '0' COMMENT '是否热门:0否,1是',
  `is_new` tinyint(1) DEFAULT '0' COMMENT '是否新品:0否,1是',
  `is_recommend` tinyint(1) DEFAULT '0' COMMENT '是否推荐:0否,1是',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0下架,1上架',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_sale` (`sale`),
  KEY `idx_price` (`price`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- 管理员表
CREATE TABLE IF NOT EXISTS `admins` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '管理员ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(64) NOT NULL COMMENT '密码',
  `name` varchar(50) DEFAULT NULL COMMENT '姓名',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `role_id` int(11) UNSIGNED DEFAULT '1' COMMENT '角色ID',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1启用',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(64) DEFAULT NULL COMMENT '最后登录IP',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_username` (`username`),
  KEY `idx_role_id` (`role_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员表';

-- 管理员角色表
CREATE TABLE IF NOT EXISTS `admin_roles` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `name` varchar(50) NOT NULL COMMENT '角色名称',
  `description` varchar(255) DEFAULT NULL COMMENT '角色描述',
  `permissions` text DEFAULT NULL COMMENT '权限,JSON格式',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员角色表';

-- 插入初始数据

-- 默认管理员角色
INSERT INTO `admin_roles` (`id`, `name`, `description`, `permissions`) VALUES
(1, '超级管理员', '拥有所有权限', '{"all": true}');

-- 默认管理员账号 (用户名: admin, 密码: admin123)
INSERT INTO `admins` (`username`, `password`, `name`, `role_id`, `status`) VALUES
('admin', MD5('admin123'), '系统管理员', 1, 1);

-- 商品分类示例数据
INSERT INTO `product_categories` (`parent_id`, `name`, `icon`, `sort_order`, `level`, `is_visible`) VALUES
(0, '手机数码', 'https://example.com/icons/digital.png', 1, 1, 1),
(0, '家用电器', 'https://example.com/icons/household.png', 2, 1, 1),
(0, '服装鞋帽', 'https://example.com/icons/clothing.png', 3, 1, 1),
(0, '美妆护肤', 'https://example.com/icons/beauty.png', 4, 1, 1),
(1, '手机', 'https://example.com/icons/phone.png', 1, 2, 1),
(1, '平板电脑', 'https://example.com/icons/tablet.png', 2, 2, 1),
(1, '笔记本', 'https://example.com/icons/laptop.png', 3, 2, 1),
(2, '电视', 'https://example.com/icons/tv.png', 1, 2, 1),
(2, '冰箱', 'https://example.com/icons/fridge.png', 2, 2, 1),
(2, '洗衣机', 'https://example.com/icons/washer.png', 3, 2, 1);

-- 商品示例数据
INSERT INTO `products` (`category_id`, `name`, `subtitle`, `main_image`, `price`, `stock`, `status`, `is_hot`, `is_recommend`) VALUES
(5, 'iPhone 13', '苹果手机 A15芯片', 'https://example.com/images/iphone13.jpg', 5999.00, 1000, 1, 1, 1),
(5, '华为P50', '华为新旗舰', 'https://example.com/images/huaweip50.jpg', 4999.00, 500, 1, 1, 1),
(6, 'iPad Air', '轻薄便携', 'https://example.com/images/ipadair.jpg', 3999.00, 800, 1, 0, 1),
(7, 'MacBook Pro', '专业办公', 'https://example.com/images/macbookpro.jpg', 8999.00, 300, 1, 0, 0),
(8, '小米电视', '全面屏设计', 'https://example.com/images/mitv.jpg', 2999.00, 400, 1, 0, 1); 