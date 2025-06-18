#!/bin/bash
# 使用Git命令行推送CLB监听器案例到GitLab

# 设置变量
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
WORK_DIR="/Users/heytea/Desktop/cursor/git 智能检测"
CLB_CASE_FILE="$WORK_DIR/risk_demo/clb_listener_update_2024.json"
GIT_REPO_DIR="/Users/heytea/gitlab/risk_demo/risk_detect"
BRANCH_NAME="clb-listener-update-$TIMESTAMP"

# 打印信息
echo "🔧 CLB监听器案例推送工具 (Git命令行版)"
echo "================================================"
echo "工作目录: $WORK_DIR"
echo "CLB案例文件: $CLB_CASE_FILE"
echo "Git仓库目录: $GIT_REPO_DIR"
echo "分支名称: $BRANCH_NAME"
echo ""

# 检查文件是否存在
if [ ! -f "$CLB_CASE_FILE" ]; then
    echo "❌ CLB案例文件不存在: $CLB_CASE_FILE"
    exit 1
fi

# 进入Git仓库目录
echo "🔍 进入Git仓库目录..."
cd "$GIT_REPO_DIR" || {
    echo "❌ 无法进入Git仓库目录: $GIT_REPO_DIR"
    exit 1
}

# 确保仓库是最新的
echo "🔄 更新Git仓库..."
git checkout main
git pull --rebase origin main

# 创建新分支
echo "🌿 创建新分支: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

# 复制CLB案例文件到仓库
echo "📝 复制CLB案例文件到仓库..."
TARGET_DIR="$GIT_REPO_DIR/risk_demo"
mkdir -p "$TARGET_DIR"
TARGET_FILE="$TARGET_DIR/clb_listener_update_$(date +"%Y%m%d").json"
cp "$CLB_CASE_FILE" "$TARGET_FILE"

# 添加到Git
echo "➕ 添加文件到Git..."
git add "$TARGET_FILE"

# 提交更改
echo "💾 提交更改..."
git commit -m "添加CLB监听器调整案例"

# 推送到远程仓库
echo "🚀 推送到远程仓库..."
git push origin "$BRANCH_NAME"

# 检查推送结果
if [ $? -eq 0 ]; then
    echo "\n✅ CLB监听器案例已成功推送到GitLab!"
    echo "请访问GitLab创建合并请求:"
    echo "http://10.251.0.16/gitlab-instance-1807000d/risk_detect/-/merge_requests/new?merge_request%5Bsource_branch%5D=$BRANCH_NAME"
    
    echo "\n🔍 检查Grafana可视化效果..."
    echo "请访问Grafana仪表盘查看可视化效果:"
    echo "URL: http://localhost:3000/d/risk-assessment/risk-assessment-dashboard"
    echo "用户名: admin"
    echo "密码: admin"
    
    echo "\n✅ 任务完成!"
else
    echo "\n❌ 推送失败!"
    exit 1
fi