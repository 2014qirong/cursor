FROM nginx:alpine

# 复制网站文件到Nginx的默认目录
COPY 案例-常用工具网站/ /usr/share/nginx/html/

# 配置Nginx
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