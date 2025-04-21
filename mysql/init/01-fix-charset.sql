USE mall_dev;

-- 使用正确的中文注释重新创建表

-- 修复 products 表的注释
ALTER TABLE products COMMENT='商品表';
ALTER TABLE products MODIFY COLUMN id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '商品ID';
ALTER TABLE products MODIFY COLUMN category_id int unsigned NOT NULL COMMENT '分类ID';
ALTER TABLE products MODIFY COLUMN name varchar(100) NOT NULL COMMENT '商品名称';
ALTER TABLE products MODIFY COLUMN subtitle varchar(200) DEFAULT NULL COMMENT '副标题';
ALTER TABLE products MODIFY COLUMN main_image varchar(255) NOT NULL COMMENT '主图';
ALTER TABLE products MODIFY COLUMN sub_images text DEFAULT NULL COMMENT '子图,JSON格式';
ALTER TABLE products MODIFY COLUMN detail text DEFAULT NULL COMMENT '商品详情';
ALTER TABLE products MODIFY COLUMN price decimal(10,2) NOT NULL COMMENT '商品价格';
ALTER TABLE products MODIFY COLUMN stock int NOT NULL COMMENT '库存';
ALTER TABLE products MODIFY COLUMN sale int DEFAULT '0' COMMENT '销量';
ALTER TABLE products MODIFY COLUMN unit varchar(20) DEFAULT NULL COMMENT '单位';
ALTER TABLE products MODIFY COLUMN weight decimal(10,2) DEFAULT NULL COMMENT '重量,单位g';
ALTER TABLE products MODIFY COLUMN is_hot tinyint(1) DEFAULT '0' COMMENT '是否热门:0否,1是';
ALTER TABLE products MODIFY COLUMN is_new tinyint(1) DEFAULT '0' COMMENT '是否新品:0否,1是';
ALTER TABLE products MODIFY COLUMN is_recommend tinyint(1) DEFAULT '0' COMMENT '是否推荐:0否,1是';
ALTER TABLE products MODIFY COLUMN status tinyint(1) DEFAULT '1' COMMENT '状态:0下架,1上架';
ALTER TABLE products MODIFY COLUMN created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间';
ALTER TABLE products MODIFY COLUMN updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间';

-- 修复 product_categories 表的注释
ALTER TABLE product_categories COMMENT='商品分类表';
ALTER TABLE product_categories MODIFY COLUMN id int unsigned NOT NULL AUTO_INCREMENT COMMENT '分类ID';
ALTER TABLE product_categories MODIFY COLUMN parent_id int unsigned DEFAULT '0' COMMENT '父分类ID,0为一级分类';
ALTER TABLE product_categories MODIFY COLUMN name varchar(50) NOT NULL COMMENT '分类名称';
ALTER TABLE product_categories MODIFY COLUMN icon varchar(255) DEFAULT NULL COMMENT '分类图标';
ALTER TABLE product_categories MODIFY COLUMN banner varchar(255) DEFAULT NULL COMMENT '分类banner图';
ALTER TABLE product_categories MODIFY COLUMN sort_order int DEFAULT '0' COMMENT '排序值,越小越靠前';
ALTER TABLE product_categories MODIFY COLUMN level tinyint(1) DEFAULT '1' COMMENT '分类级别';
ALTER TABLE product_categories MODIFY COLUMN is_visible tinyint(1) DEFAULT '1' COMMENT '是否显示:0否,1是';
ALTER TABLE product_categories MODIFY COLUMN created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间';
ALTER TABLE product_categories MODIFY COLUMN updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间';

-- 修复 users 表的注释
ALTER TABLE users COMMENT='用户表';
ALTER TABLE users MODIFY COLUMN id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID';
ALTER TABLE users MODIFY COLUMN openid varchar(64) NOT NULL COMMENT '微信openid';
ALTER TABLE users MODIFY COLUMN nickname varchar(50) DEFAULT NULL COMMENT '用户昵称';
ALTER TABLE users MODIFY COLUMN avatar varchar(255) DEFAULT NULL COMMENT '头像URL';
ALTER TABLE users MODIFY COLUMN gender tinyint(1) DEFAULT '0' COMMENT '性别:0未知,1男,2女';
ALTER TABLE users MODIFY COLUMN phone varchar(20) DEFAULT NULL COMMENT '手机号';
ALTER TABLE users MODIFY COLUMN birthday date DEFAULT NULL COMMENT '生日';
ALTER TABLE users MODIFY COLUMN points int unsigned DEFAULT '0' COMMENT '积分';
ALTER TABLE users MODIFY COLUMN balance decimal(10,2) DEFAULT '0.00' COMMENT '余额';
ALTER TABLE users MODIFY COLUMN level_id int unsigned DEFAULT '1' COMMENT '等级ID';
ALTER TABLE users MODIFY COLUMN is_disabled tinyint(1) DEFAULT '0' COMMENT '是否禁用:0否,1是';
ALTER TABLE users MODIFY COLUMN last_login_time datetime DEFAULT NULL COMMENT '最后登录时间';
ALTER TABLE users MODIFY COLUMN last_login_ip varchar(50) DEFAULT NULL COMMENT '最后登录IP';
ALTER TABLE users MODIFY COLUMN created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间';
ALTER TABLE users MODIFY COLUMN updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间';

-- 修复 admin_roles 表的注释
ALTER TABLE admin_roles COMMENT='管理员角色表';
ALTER TABLE admin_roles MODIFY COLUMN id int unsigned NOT NULL AUTO_INCREMENT COMMENT '角色ID';
ALTER TABLE admin_roles MODIFY COLUMN name varchar(50) NOT NULL COMMENT '角色名称';
ALTER TABLE admin_roles MODIFY COLUMN description varchar(255) DEFAULT NULL COMMENT '角色描述';
ALTER TABLE admin_roles MODIFY COLUMN permissions text DEFAULT NULL COMMENT '权限,JSON格式';
ALTER TABLE admin_roles MODIFY COLUMN created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间';
ALTER TABLE admin_roles MODIFY COLUMN updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间';

-- 修复 admins 表的注释
ALTER TABLE admins COMMENT='管理员表';
ALTER TABLE admins MODIFY COLUMN id int unsigned NOT NULL AUTO_INCREMENT COMMENT '管理员ID';
ALTER TABLE admins MODIFY COLUMN username varchar(50) NOT NULL COMMENT '用户名';
ALTER TABLE admins MODIFY COLUMN password varchar(64) NOT NULL COMMENT '密码';
ALTER TABLE admins MODIFY COLUMN name varchar(50) DEFAULT NULL COMMENT '姓名';
ALTER TABLE admins MODIFY COLUMN avatar varchar(255) DEFAULT NULL COMMENT '头像';
ALTER TABLE admins MODIFY COLUMN email varchar(100) DEFAULT NULL COMMENT '邮箱';
ALTER TABLE admins MODIFY COLUMN phone varchar(20) DEFAULT NULL COMMENT '手机号';
ALTER TABLE admins MODIFY COLUMN role_id int unsigned DEFAULT '1' COMMENT '角色ID';
ALTER TABLE admins MODIFY COLUMN status tinyint(1) DEFAULT '1' COMMENT '状态:0禁用,1启用';
ALTER TABLE admins MODIFY COLUMN last_login_time datetime DEFAULT NULL COMMENT '最后登录时间';
ALTER TABLE admins MODIFY COLUMN last_login_ip varchar(64) DEFAULT NULL COMMENT '最后登录IP';
ALTER TABLE admins MODIFY COLUMN created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间';
ALTER TABLE admins MODIFY COLUMN updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'; 