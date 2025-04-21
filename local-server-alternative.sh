#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # 无颜色

echo -e "${BLUE}=====================================${NC}"
echo -e "${GREEN}常用工具网站 - 本地服务器启动脚本${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# 检查是否可以使用Python
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}使用Python启动本地服务器...${NC}"
    cd 案例-常用工具网站 || { echo -e "${RED}错误：无法进入网站目录${NC}"; exit 1; }
    
    echo -e "${BLUE}服务器启动中，访问地址：${NC}${GREEN}http://localhost:8000${NC}"
    echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
    
    # 使用Python内置的HTTP服务器
    python3 -m http.server 8000
    
    exit 0
fi

# 如果Python不可用，检查是否可以使用Node.js
if command -v node &> /dev/null; then
    echo -e "${GREEN}使用Node.js启动本地服务器...${NC}"
    
    # 检查是否安装了http-server
    if ! command -v http-server &> /dev/null; then
        echo -e "${YELLOW}正在安装http-server...${NC}"
        npm install -g http-server || { echo -e "${RED}错误：无法安装http-server${NC}"; exit 1; }
    fi
    
    cd 案例-常用工具网站 || { echo -e "${RED}错误：无法进入网站目录${NC}"; exit 1; }
    
    echo -e "${BLUE}服务器启动中，访问地址：${NC}${GREEN}http://localhost:8080${NC}"
    echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
    
    # 使用http-server
    http-server -p 8080
    
    exit 0
fi

# 如果都不可用，尝试使用PHP
if command -v php &> /dev/null; then
    echo -e "${GREEN}使用PHP启动本地服务器...${NC}"
    cd 案例-常用工具网站 || { echo -e "${RED}错误：无法进入网站目录${NC}"; exit 1; }
    
    echo -e "${BLUE}服务器启动中，访问地址：${NC}${GREEN}http://localhost:8000${NC}"
    echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
    
    # 使用PHP内置的HTTP服务器
    php -S localhost:8000
    
    exit 0
fi

echo -e "${RED}错误：找不到可用的服务器。${NC}"
echo -e "${YELLOW}请安装以下工具之一：${NC}"
echo -e "  - Python 3"
echo -e "  - Node.js"
echo -e "  - PHP"
echo ""
echo -e "${BLUE}或者按照 docker-install-guide.md 中的说明安装Docker${NC}"

exit 1 