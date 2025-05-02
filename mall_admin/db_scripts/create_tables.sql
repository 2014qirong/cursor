-- 创建数据库
CREATE DATABASE IF NOT EXISTS mall_dev DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE mall_dev;

-- 用户表
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(100) NOT NULL COMMENT '用户名',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `gender` tinyint(1) DEFAULT '0' COMMENT '性别：0未知，1男，2女',
  `birthday` date DEFAULT NULL COMMENT '生日',
  `level` tinyint(1) DEFAULT '1' COMMENT '等级',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态：0禁用，1正常',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  KEY `idx_phone` (`phone`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 管理员表
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '管理员ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `name` varchar(50) DEFAULT NULL COMMENT '姓名',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `role_id` int(11) UNSIGNED DEFAULT NULL COMMENT '角色ID',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态：0禁用，1正常',
  `login_ip` varchar(50) DEFAULT NULL COMMENT '最后登录IP',
  `login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  KEY `idx_role_id` (`role_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员表';

-- 角色表
CREATE TABLE IF NOT EXISTS `role` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `name` varchar(50) NOT NULL COMMENT '角色名称',
  `description` varchar(255) DEFAULT NULL COMMENT '角色描述',
  `permissions` text COMMENT '权限列表（JSON格式）',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态：0禁用，1正常',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- 商品分类表
CREATE TABLE IF NOT EXISTS `product_category` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `parent_id` int(11) UNSIGNED DEFAULT '0' COMMENT '父分类ID',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `icon` varchar(255) DEFAULT NULL COMMENT '图标',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态：0禁用，1正常',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_sort` (`sort`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- 商品表
CREATE TABLE IF NOT EXISTS `product` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `category_id` int(11) UNSIGNED DEFAULT NULL COMMENT '分类ID',
  `name` varchar(100) NOT NULL COMMENT '商品名称',
  `subtitle` varchar(200) DEFAULT NULL COMMENT '副标题',
  `keywords` varchar(255) DEFAULT NULL COMMENT '关键字',
  `description` text COMMENT '商品描述',
  `price` decimal(10,2) NOT NULL COMMENT '价格',
  `market_price` decimal(10,2) DEFAULT NULL COMMENT '市场价',
  `stock` int(11) DEFAULT '0' COMMENT '库存',
  `sales` int(11) DEFAULT '0' COMMENT '销量',
  `main_image` varchar(255) DEFAULT NULL COMMENT '主图',
  `album` text COMMENT '相册（JSON格式）',
  `detail` text COMMENT '详情',
  `specs` text COMMENT '规格（JSON格式）',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态：0下架，1上架',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_status` (`status`),
  KEY `idx_sort` (`sort`),
  FULLTEXT KEY `ft_name_subtitle_keywords` (`name`,`subtitle`,`keywords`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- 订单表
CREATE TABLE IF NOT EXISTS `order` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_sn` varchar(64) NOT NULL COMMENT '订单编号',
  `user_id` int(11) UNSIGNED NOT NULL COMMENT '用户ID',
  `total_amount` decimal(10,2) NOT NULL COMMENT '订单总金额',
  `pay_amount` decimal(10,2) NOT NULL COMMENT '实付金额',
  `freight_amount` decimal(10,2) DEFAULT '0.00' COMMENT '运费',
  `discount_amount` decimal(10,2) DEFAULT '0.00' COMMENT '优惠金额',
  `pay_type` tinyint(1) DEFAULT NULL COMMENT '支付方式：1微信，2支付宝',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
  `status` tinyint(1) DEFAULT '0' COMMENT '订单状态：0待付款，1待发货，2已发货，3已完成，4已取消，5已退款',
  `shipping_name` varchar(50) DEFAULT NULL COMMENT '收货人姓名',
  `shipping_phone` varchar(20) DEFAULT NULL COMMENT '收货人电话',
  `shipping_address` varchar(255) DEFAULT NULL COMMENT '收货地址',
  `shipping_code` varchar(50) DEFAULT NULL COMMENT '物流单号',
  `shipping_company` varchar(50) DEFAULT NULL COMMENT '物流公司',
  `note` varchar(255) DEFAULT NULL COMMENT '订单备注',
  `confirm_time` datetime DEFAULT NULL COMMENT '确认收货时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_sn` (`order_sn`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 订单明细表
CREATE TABLE IF NOT EXISTS `order_item` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订单明细ID',
  `order_id` int(11) UNSIGNED NOT NULL COMMENT '订单ID',
  `product_id` int(11) UNSIGNED NOT NULL COMMENT '商品ID',
  `product_name` varchar(100) NOT NULL COMMENT '商品名称',
  `product_image` varchar(255) DEFAULT NULL COMMENT '商品图片',
  `product_price` decimal(10,2) NOT NULL COMMENT '商品价格',
  `quantity` int(11) NOT NULL COMMENT '购买数量',
  `specs` varchar(255) DEFAULT NULL COMMENT '规格信息',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单明细表';

-- 文章分类表
CREATE TABLE IF NOT EXISTS `article_category` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态：0禁用，1正常',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_sort` (`sort`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章分类表';

-- 文章表
CREATE TABLE IF NOT EXISTS `article` (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '文章ID',
  `category_id` int(11) UNSIGNED DEFAULT NULL COMMENT '分类ID',
  `title` varchar(100) NOT NULL COMMENT '文章标题',
  `author` varchar(50) DEFAULT NULL COMMENT '作者',
  `cover_image` varchar(255) DEFAULT NULL COMMENT '封面图片',
  `content` text NOT NULL COMMENT '文章内容',
  `summary` varchar(500) DEFAULT NULL COMMENT '摘要',
  `is_top` tinyint(1) DEFAULT '0' COMMENT '是否置顶：0否，1是',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态：0草稿，1发布',
  `view_count` int(11) DEFAULT '0' COMMENT '浏览量',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_is_top` (`is_top`),
  KEY `idx_status` (`status`),
  KEY `idx_sort` (`sort`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文章表';

-- 插入初始管理员
INSERT INTO `admin` (`username`, `password`, `name`, `status`) VALUES 
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '系统管理员', 1);

-- 插入初始角色
INSERT INTO `role` (`name`, `description`, `permissions`, `status`) VALUES 
('超级管理员', '系统超级管理员，拥有所有权限', '["*"]', 1);

-- 更新管理员角色
UPDATE `admin` SET `role_id` = 1 WHERE `username` = 'admin';

-- 插入初始商品分类
INSERT INTO `product_category` (`parent_id`, `name`, `sort`, `status`) VALUES 
(0, '家电', 1, 1),
(0, '服装', 2, 1),
(0, '食品', 3, 1),
(1, '电视', 1, 1),
(1, '冰箱', 2, 1),
(2, '男装', 1, 1),
(2, '女装', 2, 1);

-- 插入文章分类
INSERT INTO `article_category` (`name`, `sort`, `status`) VALUES 
('公司动态', 1, 1),
('行业资讯', 2, 1),
('产品教程', 3, 1),
('常见问题', 4, 1); 