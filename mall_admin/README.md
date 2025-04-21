# 商城小程序后台管理系统

基于Vue3、Element Plus、Vite构建的商城小程序管理系统。

## 技术栈

- **前端框架**：Vue.js 3 + Vite
- **UI组件库**：Element Plus
- **状态管理**：Pinia
- **路由管理**：Vue Router
- **HTTP客户端**：Axios
- **图表库**：ECharts
- **富文本编辑器**：TinyMCE
- **构建工具**：Vite

## 功能特性

- 商品管理
- 订单管理
- 用户管理
- 营销管理
- 内容管理
- 系统设置
- 统计报表

## 快速开始

### 环境准备

- Node.js (>= 16.0.0)
- npm (>= 7.0.0)

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 项目结构

```
mall_admin/
├── public/                   # 静态资源
├── src/                      # 源代码
│   ├── api/                  # API请求封装
│   ├── assets/               # 静态资源
│   ├── components/           # 通用组件
│   ├── directives/           # 自定义指令
│   ├── hooks/                # 自定义hooks
│   ├── layout/               # 布局文件
│   ├── router/               # 路由配置
│   ├── store/                # 状态管理
│   ├── utils/                # 工具函数
│   ├── views/                # 页面组件
│   ├── App.vue               # 根组件
│   ├── main.js               # 入口文件
│   └── permission.js         # 权限控制
├── .env.development          # 开发环境配置
├── .env.production           # 生产环境配置
├── .eslintrc.js              # ESLint配置
├── vite.config.js            # Vite配置
└── package.json              # 项目依赖
```

## 开发指南

### 新增页面

1. 在`src/views`目录下创建页面组件
2. 在`src/router/modules`中添加路由配置
3. 在相应模块中导入路由配置

### 添加API

1. 在`src/api`目录下创建API文件
2. 使用`utils/request.js`中的请求工具函数

### 状态管理

1. 使用Pinia创建状态
2. 在组件中通过`useStore`使用

## 项目规范

- 遵循ESLint规范
- 组件使用PascalCase命名
- 接口函数使用camelCase命名
- CSS使用BEM命名方法 