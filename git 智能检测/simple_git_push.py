#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil
from datetime import datetime

def run_command(cmd, cwd=None):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def push_database_sg_case():
    """使用Git命令推送数据库安全组变更测试用例"""
    print("🚀 开始推送数据库安全组变更测试用例到GitLab")
    print("=" * 60)
    
    # GitLab配置
    gitlab_url = "http://10.251.0.16/gitlab-instance-1807000d/risk_detect.git"
    branch_name = f"feature/database-sg-change-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    # 源文件路径
    source_dir = "/Users/heytea/Desktop/cursor/git 智能检测/gitlab_simulation/test/高风险---数据库安全组变更"
    
    # 临时工作目录
    temp_dir = "/tmp/risk_detect_push"
    
    try:
        # 清理并创建临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        print(f"📁 工作目录: {temp_dir}")
        
        # 克隆仓库
        print("\n1. 克隆GitLab仓库...")
        clone_cmd = f"git clone {gitlab_url} ."
        success, stdout, stderr = run_command(clone_cmd, temp_dir)
        if not success:
            print(f"❌ 克隆失败: {stderr}")
            return False
        print("✅ 仓库克隆成功")
        
        # 配置Git用户信息
        print("\n2. 配置Git用户信息...")
        run_command("git config user.name 'Risk Assessment Bot'", temp_dir)
        run_command("git config user.email 'risk-bot@example.com'", temp_dir)
        
        # 创建新分支
        print(f"\n3. 创建新分支: {branch_name}")
        success, stdout, stderr = run_command(f"git checkout -b {branch_name}", temp_dir)
        if not success:
            print(f"❌ 创建分支失败: {stderr}")
            return False
        print("✅ 分支创建成功")
        
        # 复制测试用例文件
        print("\n4. 复制测试用例文件...")
        target_dir = os.path.join(temp_dir, "test_cases", "database_security_group")
        os.makedirs(target_dir, exist_ok=True)
        
        # 复制文件
        files_to_copy = [
            "test_case_info.json",
            "security/database-sg-rules.json",
            "changes.diff"
        ]
        
        for file_path in files_to_copy:
            source_file = os.path.join(source_dir, file_path)
            if os.path.exists(source_file):
                target_file = os.path.join(target_dir, os.path.basename(file_path))
                # 创建目标目录
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.copy2(source_file, target_file)
                print(f"  ✅ 复制: {file_path}")
            else:
                print(f"  ⚠️  文件不存在: {file_path}")
        
        # 添加文件到Git
        print("\n5. 添加文件到Git...")
        success, stdout, stderr = run_command("git add .", temp_dir)
        if not success:
            print(f"❌ 添加文件失败: {stderr}")
            return False
        print("✅ 文件添加成功")
        
        # 提交更改
        print("\n6. 提交更改...")
        commit_msg = "feat: 添加数据库安全组变更风险评估测试用例\n\n- 新增高风险数据库安全组规则变更测试\n- 包含MySQL访问规则和SSH访问CIDR变更\n- 用于验证安全组变更的风险评估功能"
        success, stdout, stderr = run_command(f'git commit -m "{commit_msg}"', temp_dir)
        if not success:
            print(f"❌ 提交失败: {stderr}")
            return False
        print("✅ 提交成功")
        
        # 推送到远程仓库
        print("\n7. 推送到远程仓库...")
        push_cmd = f"git push origin {branch_name}"
        success, stdout, stderr = run_command(push_cmd, temp_dir)
        if not success:
            print(f"❌ 推送失败: {stderr}")
            print(f"详细错误: {stdout}")
            return False
        print("✅ 推送成功")
        
        print(f"\n🎉 数据库安全组变更测试用例推送完成!")
        print(f"📋 分支名称: {branch_name}")
        print(f"🔗 GitLab地址: http://10.251.0.16/gitlab-instance-1807000d/risk_detect")
        
        return True
        
    except Exception as e:
        print(f"❌ 推送过程中发生异常: {str(e)}")
        return False
    finally:
        # 清理临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"\n🧹 清理临时目录: {temp_dir}")

if __name__ == "__main__":
    success = push_database_sg_case()
    if success:
        print("\n✅ 推送任务完成")
    else:
        print("\n❌ 推送任务失败")