#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # 无颜色

echo -e "${BLUE}=====================================${NC}"
echo -e "${GREEN}常用工具网站 - 本地部署启动脚本${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误：Docker未安装。请先安装Docker: https://www.docker.com/get-started${NC}"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}警告：Docker Compose未安装。将使用普通Docker命令启动。${NC}"
    
    echo -e "${BLUE}正在构建Docker镜像...${NC}"
    docker build -t web-tools .
    
    echo -e "${BLUE}正在启动容器...${NC}"
    docker run -d -p 8080:80 --name web-tools-app web-tools
else
    echo -e "${BLUE}正在使用Docker Compose启动服务...${NC}"
    docker-compose up -d
fi

# 检查启动是否成功
sleep 3
if docker ps | grep -q "web-tools-app"; then
    echo -e "${GREEN}服务启动成功！${NC}"
    echo -e "${GREEN}请访问 http://localhost:8080 使用工具集网站${NC}"
    
    # 尝试自动打开浏览器
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8080
    elif command -v open &> /dev/null; then
        open http://localhost:8080
    elif command -v start &> /dev/null; then
        start http://localhost:8080
    fi
else
    echo -e "${RED}服务启动失败！请检查日志获取更多信息。${NC}"
    echo -e "${BLUE}可以尝试运行以下命令查看日志：${NC}"
    echo "docker logs web-tools-app"
fi

echo ""
echo -e "${BLUE}=====================================${NC}"
echo -e "${GREEN}要停止服务，请运行以下命令之一：${NC}"
echo -e "${BLUE}- Docker Compose: ${NC}docker-compose down"
echo -e "${BLUE}- 仅Docker: ${NC}docker stop web-tools-app && docker rm web-tools-app"
echo -e "${BLUE}=====================================${NC}" 