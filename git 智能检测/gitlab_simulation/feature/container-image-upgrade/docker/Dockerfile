# 测试用例: 中风险 - 容器镜像版本升级
# 风险等级: medium
# 升级基础镜像版本，包含安全补丁

# 升级基础镜像从 node:18.17.0-alpine 到 node:18.19.0-alpine
FROM node:18.19.0-alpine

# 设置工作目录
WORKDIR /app

# 安装安全更新
RUN apk update && apk upgrade && \
    apk add --no-cache \
    curl \
    ca-certificates && \
    rm -rf /var/cache/apk/*

# 复制package文件
COPY package*.json ./

# 安装依赖，使用npm audit fix修复安全漏洞
RUN npm ci --only=production && \
    npm audit fix && \
    npm cache clean --force

# 复制应用代码
COPY src/ ./src/
COPY config/ ./config/

# 创建非root用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# 设置文件权限
RUN chown -R nextjs:nodejs /app
USER nextjs

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# 启动应用
CMD ["node", "src/server.js"]