SET NAMES utf8mb4;
USE mall_dev;

-- 1. 修复 products 表
DROP TABLE IF EXISTS products_new;
CREATE TABLE products_new (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `category_id` int unsigned NOT NULL COMMENT '分类ID',
  `name` varchar(100) NOT NULL COMMENT '商品名称',
  `subtitle` varchar(200) DEFAULT NULL COMMENT '副标题',
  `main_image` varchar(255) NOT NULL COMMENT '主图',
  `sub_images` text DEFAULT NULL COMMENT '子图,JSON格式',
  `detail` text DEFAULT NULL COMMENT '商品详情',
  `price` decimal(10,2) NOT NULL COMMENT '商品价格',
  `stock` int NOT NULL COMMENT '库存',
  `sale` int DEFAULT '0' COMMENT '销量',
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品表';

-- 复制原表数据
INSERT INTO products_new SELECT * FROM products;
RENAME TABLE products TO products_old, products_new TO products;
DROP TABLE products_old;

-- 2. 修复 product_categories 表
DROP TABLE IF EXISTS product_categories_new;
CREATE TABLE product_categories_new (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `parent_id` int unsigned DEFAULT '0' COMMENT '父分类ID,0为一级分类',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `icon` varchar(255) DEFAULT NULL COMMENT '分类图标',
  `banner` varchar(255) DEFAULT NULL COMMENT '分类banner图',
  `sort_order` int DEFAULT '0' COMMENT '排序值,越小越靠前',
  `level` tinyint(1) DEFAULT '1' COMMENT '分类级别',
  `is_visible` tinyint(1) DEFAULT '1' COMMENT '是否显示:0否,1是',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_sort` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品分类表';

INSERT INTO product_categories_new SELECT * FROM product_categories;
RENAME TABLE product_categories TO product_categories_old, product_categories_new TO product_categories;
DROP TABLE product_categories_old;

-- 3. 修复 admin_roles 表
DROP TABLE IF EXISTS admin_roles_new;
CREATE TABLE admin_roles_new (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `name` varchar(50) NOT NULL COMMENT '角色名称',
  `description` varchar(255) DEFAULT NULL COMMENT '角色描述',
  `permissions` text DEFAULT NULL COMMENT '权限,JSON格式',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员角色表';

INSERT INTO admin_roles_new SELECT * FROM admin_roles;
RENAME TABLE admin_roles TO admin_roles_old, admin_roles_new TO admin_roles;
DROP TABLE admin_roles_old;

-- 4. 修复 admins 表
DROP TABLE IF EXISTS admins_new;
CREATE TABLE admins_new (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '管理员ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(64) NOT NULL COMMENT '密码',
  `name` varchar(50) DEFAULT NULL COMMENT '姓名',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `role_id` int unsigned DEFAULT '1' COMMENT '角色ID',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1启用',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(64) DEFAULT NULL COMMENT '最后登录IP',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_username` (`username`),
  KEY `idx_role_id` (`role_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员表';

INSERT INTO admins_new SELECT * FROM admins;
RENAME TABLE admins TO admins_old, admins_new TO admins;
DROP TABLE admins_old;

-- 5. 修复 users 表
DROP TABLE IF EXISTS users_new;
CREATE TABLE users_new (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `openid` varchar(64) NOT NULL COMMENT '微信openid',
  `nickname` varchar(50) DEFAULT NULL COMMENT '用户昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像URL',
  `gender` tinyint(1) DEFAULT '0' COMMENT '性别:0未知,1男,2女',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `points` int unsigned DEFAULT '0' COMMENT '积分',
  `balance` decimal(10,2) DEFAULT '0.00' COMMENT '余额',
  `level_id` int unsigned DEFAULT '1' COMMENT '等级ID',
  `is_disabled` tinyint(1) DEFAULT '0' COMMENT '是否禁用:0否,1是',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(50) DEFAULT NULL COMMENT '最后登录IP',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_openid` (`openid`),
  KEY `idx_phone` (`phone`),
  KEY `idx_level_id` (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

INSERT INTO users_new SELECT * FROM users;
RENAME TABLE users TO users_old, users_new TO users;
DROP TABLE users_old; 