#!/bin/bash

echo "正在停止开发环境容器..."
docker-compose -f docker-compose.dev.yml down

echo "开发环境已停止!" 