-- 设置客户端字符集
SET NAMES utf8mb4;

-- 查看数据库字符集
ALTER DATABASE mall_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 修复表的字符集
USE mall_dev;

ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE admins CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE admin_roles CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE products CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE product_categories CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 重新插入中文数据
TRUNCATE TABLE products;
INSERT INTO products (category_id, name, subtitle, main_image, price, stock, status, is_hot, is_recommend) VALUES
(5, 'iPhone 13', '苹果手机 A15芯片', 'https://example.com/images/iphone13.jpg', 5999.00, 1000, 1, 1, 1),
(5, '华为P50', '华为新旗舰', 'https://example.com/images/huaweip50.jpg', 4999.00, 500, 1, 1, 1),
(6, 'iPad Air', '轻薄便携', 'https://example.com/images/ipadair.jpg', 3999.00, 800, 1, 0, 1),
(7, 'MacBook Pro', '专业办公', 'https://example.com/images/macbookpro.jpg', 8999.00, 300, 1, 0, 0),
(8, '小米电视', '全面屏设计', 'https://example.com/images/mitv.jpg', 2999.00, 400, 1, 0, 1);

TRUNCATE TABLE product_categories;
INSERT INTO product_categories (parent_id, name, icon, sort_order, level, is_visible) VALUES
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

TRUNCATE TABLE admin_roles;
INSERT INTO admin_roles (id, name, description, permissions) VALUES
(1, '超级管理员', '拥有所有权限', '{"all": true}');

TRUNCATE TABLE admins;
INSERT INTO admins (username, password, name, role_id, status) VALUES
('admin', MD5('admin123'), '系统管理员', 1, 1); 