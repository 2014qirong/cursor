# 商城小程序开发环境配置

本文档描述如何使用Docker容器化方式快速搭建商城小程序的开发环境。

## 目录结构

```
环境与配置设计/
├── docker-compose.dev.yml     # 开发环境Docker Compose配置
├── .env.development           # 开发环境变量配置
├── mysql/                     # MySQL相关配置
│   ├── conf/                  # MySQL配置文件
│   │   └── my.cnf             # MySQL配置
│   └── init/                  # MySQL初始化脚本
│       └── 00-create-databases.sql  # 初始化数据库脚本
├── elasticsearch/             # Elasticsearch相关配置
│   └── config/                # Elasticsearch配置文件
│       └── elasticsearch.yml  # Elasticsearch配置
├── start-dev-env.sh           # 启动开发环境脚本
└── stop-dev-env.sh            # 停止开发环境脚本
```

## 环境组件

开发环境包含以下组件：

- **MySQL 8.0**: 主要数据库，端口 3306
- **Redis 6.0**: 缓存数据库，端口 6379
- **Elasticsearch 7.14.0**: 搜索引擎，端口 9200
- **Kibana 7.14.0**: Elasticsearch管理工具，端口 5601
- **Adminer**: MySQL管理工具，端口 8080
- **Redis Commander**: Redis管理工具，端口 8081

## 快速开始

### 前置条件

- 安装 [Docker](https://www.docker.com/get-started)
- 安装 [Docker Compose](https://docs.docker.com/compose/install/)

### 启动环境

1. 确保您已安装Docker和Docker Compose
2. 在终端中执行以下命令：

```bash
# 添加执行权限
chmod +x start-dev-env.sh stop-dev-env.sh

# 启动开发环境
./start-dev-env.sh
```

### 停止环境

```bash
./stop-dev-env.sh
```

## 访问信息

启动环境后，可以通过以下地址访问各个服务：

| 服务 | 地址 | 用户名 | 密码 |
|-----|------|-------|------|
| MySQL | localhost:3306 | dev_user | admin123 |
| Redis | localhost:6379 | - | admin123 |
| Elasticsearch | http://localhost:9200 | - | - |
| Kibana | http://localhost:5601 | - | - |
| Adminer (MySQL管理) | http://localhost:8080 | dev_user | admin123 |
| Redis Commander | http://localhost:8081 | - | - |

## 数据库信息

- **数据库名**: mall_dev
- **默认管理员**: 
  - 用户名: admin
  - 密码: admin123

## 环境变量配置

开发环境的环境变量配置位于 `.env.development` 文件中，主要包含：

- API服务配置
- 数据库配置
- Redis配置
- Elasticsearch配置
- 上传配置
- JWT配置
- 微信小程序配置
- 日志配置

## 使用说明

### MySQL

通过Adminer进行管理：
1. 访问 http://localhost:8080
2. 登录类型选择 MySQL
3. 服务器: mysql (在docker网络中)或 localhost (在主机)
4. 用户名: dev_user
5. 密码: admin123
6. 数据库: mall_dev

### Redis

通过Redis Commander进行管理：
1. 访问 http://localhost:8081
2. 连接信息已预先配置

### Elasticsearch

通过Kibana进行管理：
1. 访问 http://localhost:5601
2. 配置索引模式开始使用

## 数据持久化

所有数据都存储在Docker卷中，即使容器停止或删除，数据也不会丢失。卷包括：

- mysql-data: MySQL数据
- redis-data: Redis数据
- elasticsearch-data: Elasticsearch数据

## 注意事项

1. 此环境仅用于开发和测试，不适用于生产环境
2. 默认密码仅用于开发环境，生产环境应使用强密码
3. 首次启动Elasticsearch可能需要较长时间，请耐心等待 修改Docker配置以使用阿里云镜像源
