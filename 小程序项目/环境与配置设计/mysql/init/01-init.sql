-- 创建订单表
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

-- 创建订单商品表
CREATE TABLE IF NOT EXISTS `order_items` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订单商品ID',
  `order_id` bigint(20) UNSIGNED NOT NULL COMMENT '订单ID',
  `order_no` varchar(32) NOT NULL COMMENT '订单编号',
  `product_id` bigint(20) UNSIGNED NOT NULL COMMENT '商品ID',
  `product_name` varchar(100) NOT NULL COMMENT '商品名称',
  `product_image` varchar(255) DEFAULT NULL COMMENT '商品图片',
  `sku_id` bigint(20) UNSIGNED NOT NULL COMMENT 'SKU ID',
  `sku_spec` varchar(255) DEFAULT NULL COMMENT 'SKU规格描述',
  `price` decimal(10,2) NOT NULL COMMENT '商品单价',
  `quantity` int(11) NOT NULL COMMENT '购买数量',
  `total_price` decimal(10,2) NOT NULL COMMENT '商品总价',
  `review_status` tinyint(1) DEFAULT '0' COMMENT '评价状态:0未评价,1已评价',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_order_no` (`order_no`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_sku_id` (`sku_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单商品表';

-- 创建购物车表
CREATE TABLE IF NOT EXISTS `carts` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '购物车ID',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `product_id` bigint(20) UNSIGNED NOT NULL COMMENT '商品ID',
  `sku_id` bigint(20) UNSIGNED NOT NULL COMMENT 'SKU ID',
  `quantity` int(11) NOT NULL DEFAULT '1' COMMENT '商品数量',
  `selected` tinyint(1) DEFAULT '1' COMMENT '是否选中:0否,1是',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_sku` (`user_id`,`sku_id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表';

-- 创建支付记录表
CREATE TABLE IF NOT EXISTS `payments` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '支付ID',
  `payment_no` varchar(64) NOT NULL COMMENT '支付流水号',
  `order_no` varchar(32) NOT NULL COMMENT '订单编号',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `amount` decimal(10,2) NOT NULL COMMENT '支付金额',
  `payment_type` tinyint(1) NOT NULL COMMENT '支付方式:1微信,2余额',
  `payment_status` tinyint(1) DEFAULT '0' COMMENT '支付状态:0未支付,1支付成功,2支付失败',
  `transaction_id` varchar(64) DEFAULT NULL COMMENT '第三方支付流水号',
  `payment_time` datetime DEFAULT NULL COMMENT '支付时间',
  `error_msg` varchar(255) DEFAULT NULL COMMENT '错误信息',
  `notify_time` datetime DEFAULT NULL COMMENT '回调时间',
  `notify_data` text DEFAULT NULL COMMENT '回调数据',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_payment_no` (`payment_no`),
  KEY `idx_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_payment_status` (`payment_status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付记录表';

-- 创建退款表
CREATE TABLE IF NOT EXISTS `refunds` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '退款ID',
  `refund_no` varchar(64) NOT NULL COMMENT '退款单号',
  `order_no` varchar(32) NOT NULL COMMENT '订单编号',
  `payment_no` varchar(64) NOT NULL COMMENT '支付流水号',
  `user_id` bigint(20) UNSIGNED NOT NULL COMMENT '用户ID',
  `amount` decimal(10,2) NOT NULL COMMENT '退款金额',
  `reason` varchar(255) NOT NULL COMMENT '退款原因',
  `description` varchar(500) DEFAULT NULL COMMENT '详细描述',
  `images` varchar(1000) DEFAULT NULL COMMENT '图片URL,多个以逗号分隔',
  `status` tinyint(1) DEFAULT '0' COMMENT '退款状态:0申请中,1已同意,2已拒绝,3已退款',
  `refund_time` datetime DEFAULT NULL COMMENT '退款时间',
  `reject_reason` varchar(255) DEFAULT NULL COMMENT '拒绝原因',
  `transaction_id` varchar(64) DEFAULT NULL COMMENT '第三方退款流水号',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_refund_no` (`refund_no`),
  KEY `idx_order_no` (`order_no`),
  KEY `idx_payment_no` (`payment_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='退款表';

-- 创建支付方式配置表
CREATE TABLE IF NOT EXISTS `payment_methods` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `code` varchar(50) NOT NULL COMMENT '支付方式代码',
  `name` varchar(100) NOT NULL COMMENT '支付方式名称',
  `description` varchar(255) DEFAULT NULL COMMENT '支付方式描述',
  `icon` varchar(255) DEFAULT NULL COMMENT '图标URL',
  `config` text DEFAULT NULL COMMENT '配置信息(JSON格式)',
  `fee` decimal(5,2) DEFAULT '0.00' COMMENT '手续费率(%)',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1启用',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付方式配置表';

-- 插入默认支付方式数据
INSERT INTO `payment_methods` (`code`, `name`, `description`, `icon`, `config`, `fee`, `sort`, `status`)
VALUES 
('alipay', '支付宝', '支持支付宝APP、扫码、网页支付', 'https://img.alicdn.com/imgextra/i4/O1CN01XWg0YS1YQIDyQBBvr_!!6000000003050-2-tps-200-200.png', '{"appId":"2016xxxxxxxx","publicKey":"MIIBIjANBgkqhkiG9w0BAQEF...","privateKey":"MIIEvQIBADANBgkqhkiG9w0BAQEF...","notifyUrl":"https://yourdomain.com/api/payment/alipay/notify","sandbox":true}', 0.60, 1, 1),
('wechat', '微信支付', '支持微信扫码、公众号、小程序支付', 'https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico', '{"mchId":"1900xxxxxx","mchKey":"xxxxxxxxxxxxxxxxx","appId":"wxxxxxxxxxxx","appSecret":"xxxxxxxxxxxxxx","notifyUrl":"https://yourdomain.com/api/payment/wechat/notify","sandbox":true}', 0.60, 2, 1),
('unionpay', '银联支付', '支持银联卡支付，包括借记卡和信用卡', 'https://mdn.alipayobjects.com/huamei_ptpmx/afts/img/A*tQ9VQZ26jgQAAAAAAAAAAAAADvl6AQ/original', null, 0.50, 3, 1),
('cod', '货到付款', '送货上门后现金支付给快递员', null, null, 0.00, 4, 1),
('balance', '余额支付', '使用账户余额支付', null, null, 0.00, 5, 1);

-- 创建物流公司表
CREATE TABLE IF NOT EXISTS `logistics_companies` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `code` varchar(50) NOT NULL COMMENT '物流公司代码',
  `name` varchar(100) NOT NULL COMMENT '物流公司名称',
  `logo` varchar(255) DEFAULT NULL COMMENT 'Logo URL',
  `phone` varchar(20) DEFAULT NULL COMMENT '客服电话',
  `website` varchar(255) DEFAULT NULL COMMENT '官网',
  `api_code` varchar(50) DEFAULT NULL COMMENT 'API查询代码',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1启用',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='物流公司表';

-- 插入默认物流公司数据
INSERT INTO `logistics_companies` (`code`, `name`, `logo`, `phone`, `website`, `api_code`, `sort`, `status`)
VALUES 
('SF', '顺丰速运', 'https://www.sf-express.com/sf-logo.png', '95338', 'https://www.sf-express.com', 'SF', 1, 1),
('ZTO', '中通快递', 'https://www.zto.com/zto-logo.png', '95311', 'https://www.zto.com', 'ZTO', 2, 1),
('YTO', '圆通速递', 'https://www.yto.net.cn/yto-logo.png', '95554', 'https://www.yto.net.cn', 'YTO', 3, 1),
('YD', '韵达速递', 'https://www.yundaex.com/yunda-logo.png', '95546', 'https://www.yundaex.com', 'YD', 4, 1),
('JD', '京东物流', 'https://www.jdl.com/jd-logo.png', '950616', 'https://www.jdl.com', 'JD', 5, 1);

-- 创建用户表（如果不存在）
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `open_id` varchar(64) NOT NULL COMMENT '微信OpenID',
  `union_id` varchar(64) DEFAULT NULL COMMENT '微信UnionID',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像URL',
  `gender` tinyint(1) DEFAULT '0' COMMENT '性别:0未知,1男,2女',
  `mobile` varchar(15) DEFAULT NULL COMMENT '手机号',
  `balance` decimal(10,2) DEFAULT '0.00' COMMENT '账户余额',
  `points` int(11) DEFAULT '0' COMMENT '积分',
  `level` tinyint(1) DEFAULT '0' COMMENT '会员等级',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1正常',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_open_id` (`open_id`),
  KEY `idx_mobile` (`mobile`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 创建商品分类表
CREATE TABLE IF NOT EXISTS `product_categories` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `parent_id` bigint(20) UNSIGNED DEFAULT '0' COMMENT '父分类ID,0为顶级分类',
  `name` varchar(100) NOT NULL COMMENT '分类名称',
  `icon` varchar(255) DEFAULT NULL COMMENT '分类图标',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1启用',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_sort` (`sort`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- 创建商品表
CREATE TABLE IF NOT EXISTS `products` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `category_id` bigint(20) UNSIGNED NOT NULL COMMENT '分类ID',
  `name` varchar(200) NOT NULL COMMENT '商品名称',
  `cover` varchar(255) NOT NULL COMMENT '商品主图',
  `gallery` varchar(1000) DEFAULT NULL COMMENT '商品图片,多个以逗号分隔',
  `brief` varchar(200) DEFAULT NULL COMMENT '简短描述',
  `description` text DEFAULT NULL COMMENT '详细描述',
  `price` decimal(10,2) NOT NULL COMMENT '商品价格',
  `market_price` decimal(10,2) DEFAULT NULL COMMENT '市场价格',
  `stock` int(11) DEFAULT '0' COMMENT '库存',
  `sales` int(11) DEFAULT '0' COMMENT '销量',
  `unit` varchar(20) DEFAULT NULL COMMENT '单位',
  `weight` decimal(10,2) DEFAULT NULL COMMENT '重量(kg)',
  `is_new` tinyint(1) DEFAULT '0' COMMENT '是否新品:0否,1是',
  `is_hot` tinyint(1) DEFAULT '0' COMMENT '是否热销:0否,1是',
  `is_recommend` tinyint(1) DEFAULT '0' COMMENT '是否推荐:0否,1是',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0下架,1上架',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_status` (`status`),
  KEY `idx_is_new` (`is_new`),
  KEY `idx_is_hot` (`is_hot`),
  KEY `idx_is_recommend` (`is_recommend`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- 创建轮播图表
CREATE TABLE IF NOT EXISTS `banners` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `title` varchar(100) NOT NULL COMMENT '轮播标题',
  `img_url` varchar(255) NOT NULL COMMENT '图片URL',
  `type` tinyint(1) DEFAULT '1' COMMENT '类型:1商品,2专题,3外部链接',
  `url` varchar(255) DEFAULT NULL COMMENT '链接地址',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1启用',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_sort` (`sort`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='轮播图表';

-- 插入示例轮播图数据
INSERT INTO `banners` (`title`, `img_url`, `type`, `url`, `sort`, `status`)
VALUES 
('新款春季上新', 'https://img.alicdn.com/imgextra/i1/O1CN01b5kcx91W9jOFbQ0Kn_!!6000000002744-2-tps-1125-352.png', 1, '/product/123', 1, 1),
('618年中大促', 'https://img.alicdn.com/imgextra/i2/O1CN010ThlMq1jaUNV9SU5B_!!6000000004576-0-tps-1920-600.jpg', 2, '/topic/618', 2, 1),
('品牌专场', 'https://img.alicdn.com/imgextra/i1/O1CN01MRVFUV1FGWvCBgn8i_!!6000000000463-2-tps-1125-352.png', 3, 'https://www.example.com/brand', 3, 0);

-- 创建推荐位表
CREATE TABLE IF NOT EXISTS `recommends` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(100) NOT NULL COMMENT '推荐位名称',
  `code` varchar(50) NOT NULL COMMENT '推荐位标识',
  `type` tinyint(1) DEFAULT '1' COMMENT '类型:1首页,2分类页,3专题页,4其他',
  `sort` int(11) DEFAULT '0' COMMENT '排序',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1启用',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code` (`code`),
  KEY `idx_sort` (`sort`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='推荐位表';

-- 插入示例推荐位数据
INSERT INTO `recommends` (`name`, `code`, `type`, `sort`, `status`, `remark`)
VALUES 
('首页轮播下方推荐', 'home_banner_bottom', 1, 1, 1, '首页轮播图下方的推荐商品位'),
('首页人气推荐', 'home_popular', 1, 2, 1, '首页人气推荐商品位'),
('首页新品推荐', 'home_new', 1, 3, 1, '首页新品推荐商品位'),
('分类页热门推荐', 'category_hot', 2, 1, 0, '分类页顶部热门推荐'); 