#!/bin/bash

# 进入脚本所在目录
cd "$(dirname "$0")"

echo "启动开发环境..."
echo "正在启动MySQL、Redis、Elasticsearch和管理工具..."

# 启动docker compose环境
docker compose -f docker-compose.dev.yml up -d

# 等待服务启动
echo "等待服务启动..."
sleep 5

# 检查服务状态
echo "检查服务状态..."
docker compose -f docker-compose.dev.yml ps

echo "开发环境启动完成！"
echo "可通过以下地址访问服务："
echo "- MySQL数据库: localhost:3306"
echo "- Redis: localhost:6379"
echo "- Elasticsearch: localhost:9200"
echo "- Adminer(数据库管理): http://localhost:8080"
echo "- Redis Commander: http://localhost:8081"
echo "- Kibana: http://localhost:5601" 