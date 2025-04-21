FROM node:16-alpine as build

# 设置工作目录
WORKDIR /app

# 复制package.json
COPY package.json .

# 安装依赖
RUN npm install

# 复制所有文件
COPY . .

# 构建应用
RUN npm run build

# 生产环境
FROM nginx:alpine

# 从构建阶段复制构建产物到nginx
COPY --from=build /app/dist /usr/share/nginx/html

# 配置nginx
RUN echo 'server { \
    listen       80; \
    server_name  localhost; \
    \
    location / { \
        root   /usr/share/nginx/html; \
        index  index.html; \
        try_files $uri $uri/ /index.html; \
    } \
    \
    error_page   500 502 503 504  /50x.html; \
    location = /50x.html { \
        root   /usr/share/nginx/html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 