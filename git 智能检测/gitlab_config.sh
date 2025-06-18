#!/bin/bash
# GitLab配置文件 - 腾讯云API网关测试用例推送
# 使用真实的GitLab仓库配置

# GitLab服务器地址
export GITLAB_URL='http://10.251.0.16/gitlab-instance-1807000d'

# GitLab项目ID
# 项目名称: risk_detect
export GITLAB_PROJECT_ID='risk_detect'

# GitLab用户名密码认证
export GITLAB_USERNAME='root'
export GITLAB_PASSWORD='Admin123$%'

# GitLab访问令牌（备用认证方式）
# export GITLAB_ACCESS_TOKEN='8G2btCdXRKsg-nbZxFj_'

# 自动推送规则配置
export GITLAB_AUTO_PUSH_TO_MAIN=true
export GITLAB_SKIP_CONFIRMATION=true
export GITLAB_DEFAULT_BRANCH="main"

# 使用方法：
# 1. 修改上述GITLAB_ACCESS_TOKEN为您的实际访问令牌
# 2. 运行: source gitlab_config.sh
# 3. 运行: python3 push_to_gitlab.py

echo "GitLab环境变量已设置:"
echo "GITLAB_URL: $GITLAB_URL"
echo "GITLAB_PROJECT_ID: $GITLAB_PROJECT_ID"
echo "GITLAB_USERNAME: $GITLAB_USERNAME"
echo "GITLAB_PASSWORD: ${GITLAB_PASSWORD:0:5}..."

# 验证环境变量是否设置
if [[ -z "$GITLAB_URL" || -z "$GITLAB_PROJECT_ID" || -z "$GITLAB_USERNAME" || -z "$GITLAB_PASSWORD" ]]; then
    echo "❌ 请确保所有环境变量都已正确设置"
    exit 1
else
    echo "✅ 环境变量设置完成，可以运行推送脚本了"
fi

# 获取GitLab项目信息（用于验证配置）
echo "\n🔍 验证GitLab连接..."
curl -s -u "$GITLAB_USERNAME:$GITLAB_PASSWORD" "$GITLAB_URL/api/v4/projects/$GITLAB_PROJECT_ID" | head -n 5