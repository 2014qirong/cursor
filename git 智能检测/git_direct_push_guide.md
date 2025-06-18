# GitLab 直接推送指南

## 使用 git 命令直接推送到 GitLab 仓库

### 基本步骤

1. **初始化或进入 git 仓库目录**
```bash
cd /path/to/your/project
# 如果还没有初始化 git 仓库
git init
```

2. **配置远程仓库**
```bash
# 添加 GitLab 远程仓库
git remote add origin http://10.251.0.16/gitlab-instance-1807000d/your-project.git

# 或者如果已经存在，更新远程仓库地址
git remote set-url origin http://10.251.0.16/gitlab-instance-1807000d/your-project.git
```

3. **添加文件并提交**
```bash
# 添加所有文件
git add .

# 或者添加特定文件
git add filename.txt

# 提交更改
git commit -m "Your commit message"
```

4. **推送到远程仓库**
```bash
# 推送到 main 分支
git push origin main

# 第一次推送时可能需要设置上游分支
git push -u origin main
```

### 认证配置

如果需要认证，可以使用以下方式：

1. **使用用户名密码**
```bash
git push http://username:password@10.251.0.16/gitlab-instance-1807000d/your-project.git main
```

2. **配置 git 凭据**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 示例工作流

```bash
# 1. 进入项目目录
cd /Users/heytea/Desktop/cursor/git\ 智能检测

# 2. 检查当前状态
git status

# 3. 添加新文件或修改的文件
git add .

# 4. 提交更改
git commit -m "Add risk assessment test data"

# 5. 推送到 GitLab
git push origin main
```

### 注意事项

- 确保 GitLab 服务器可访问
- 确保有推送权限
- 使用正确的分支名称（main 或 master）
- 提交信息要清晰描述更改内容

### 常用 git 命令

```bash
# 查看远程仓库
git remote -v

# 查看分支
git branch -a

# 切换分支
git checkout branch-name

# 创建并切换到新分支
git checkout -b new-branch

# 查看提交历史
git log --oneline

# 查看文件状态
git status
```

这种方式比使用 Python 脚本更直接、更标准，是 Git 的原生推送方式。