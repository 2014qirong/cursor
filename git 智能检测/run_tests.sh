#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 测试目录
TEST_DIR="test_results"
mkdir -p $TEST_DIR

# 检查服务状态
echo -e "${BLUE}检查服务状态...${NC}"

# 检查AI推理服务
AI_SERVICE_RUNNING=false
if curl -s http://localhost:8001/health > /dev/null; then
    echo -e "${GREEN}✓ AI推理服务正在运行${NC}"
    AI_SERVICE_RUNNING=true
else
    echo -e "${RED}✗ AI推理服务未运行${NC}"
fi

# 检查LIME解释服务
LIME_SERVICE_RUNNING=false
if curl -s http://localhost:8002/health > /dev/null; then
    echo -e "${GREEN}✓ LIME解释服务正在运行${NC}"
    LIME_SERVICE_RUNNING=true
else
    echo -e "${RED}✗ LIME解释服务未运行${NC}"
fi

echo ""

# 测试云变更风险预测 - K8s部署
echo -e "${BLUE}测试K8s部署变更风险预测...${NC}"
python risk_predictor.py test_k8s_deployment.yaml > test_results/k8s_result.log 2>&1
echo "K8s部署变更风险等级:"
grep "风险等级" test_results/k8s_result.log || echo -e "${YELLOW}未检测到风险等级${NC}"
echo "K8s部署变更场景描述:"
grep "场景描述" test_results/k8s_result.log || echo -e "${YELLOW}未检测到场景描述${NC}"
echo ""

# 测试云变更风险预测 - 数据库变更
echo -e "${BLUE}测试数据库变更风险预测...${NC}"
python risk_predictor.py test_database_change.tf > test_results/db_result.log 2>&1
echo "数据库变更风险等级:"
grep "风险等级" test_results/db_result.log || echo -e "${YELLOW}未检测到风险等级${NC}"
echo "数据库变更场景描述:"
grep "场景描述" test_results/db_result.log || echo -e "${YELLOW}未检测到场景描述${NC}"
echo ""

# 测试云变更风险预测 - 安全组规则
echo -e "${BLUE}测试安全组规则变更风险预测...${NC}"
python risk_predictor.py test_sg_rules.json > test_results/sg_result.log 2>&1
echo "安全组规则变更风险等级:"
grep "风险等级" test_results/sg_result.log || echo -e "${YELLOW}未检测到风险等级${NC}"
echo "安全组规则变更场景描述:"
grep "场景描述" test_results/sg_result.log || echo -e "${YELLOW}未检测到场景描述${NC}"
echo ""

# 测试云变更风险预测 - CDN配置
echo -e "${BLUE}测试CDN配置变更风险预测...${NC}"
python risk_predictor.py test_cdn_config.yaml > test_results/cdn_result.log 2>&1
echo "CDN配置变更风险等级:"
grep "风险等级" test_results/cdn_result.log || echo -e "${YELLOW}未检测到风险等级${NC}"
echo "CDN配置变更场景描述:"
grep "场景描述" test_results/cdn_result.log || echo -e "${YELLOW}未检测到场景描述${NC}"
echo ""

# 运行Python测试模块
if $AI_SERVICE_RUNNING && $LIME_SERVICE_RUNNING; then
    echo -e "${BLUE}运行Python测试模块...${NC}"
    echo -e "${YELLOW}运行test_cloud_changes.py...${NC}"
    python tests/test_cloud_changes.py > test_results/python_test_cloud.log 2>&1
    echo -e "${YELLOW}运行test_cdn_changes.py...${NC}"
    python tests/test_cdn_changes.py > test_results/python_test_cdn.log 2>&1
else
    echo -e "${RED}跳过Python测试模块 - AI服务或LIME服务未运行${NC}"
fi

echo -e "${GREEN}所有测试完成，结果保存在 $TEST_DIR 目录${NC}"

# 第二部分：使用Python测试模块进行测试
if [ "$AI_SERVICE_RUNNING" = true ] && [ "$LIME_SERVICE_RUNNING" = true ]; then
    echo -e "\n${BLUE}2. 使用Python测试模块测试${NC}"
    
    echo -e "\n${YELLOW}运行云资源变更测试...${NC}"
    python -m tests.test_cloud_changes > test_results/cloud_changes_test.log 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 测试完成${NC}"
    else
        echo -e "${RED}✗ 测试失败${NC}"
    fi
else
    echo -e "\n${YELLOW}跳过Python测试模块测试 - 服务未运行${NC}"
fi

# 结果汇总
echo -e "\n${BLUE}====================================${NC}"
echo -e "${BLUE}            测试结果              ${NC}"
echo -e "${BLUE}====================================${NC}"

echo -e "\n${YELLOW}所有测试完成，结果保存在 test_results 目录中${NC}"
echo -e "${YELLOW}以下是每个测试的简要结果：${NC}"

echo -e "\n${BLUE}=== K8s 部署变更 ===${NC}"
grep "风险等级\|场景描述" test_results/k8s_result.log

echo -e "\n${BLUE}=== 数据库变更 ===${NC}"
grep "风险等级\|场景描述" test_results/db_result.log

echo -e "\n${BLUE}=== 安全组规则变更 ===${NC}"
grep "风险等级\|场景描述" test_results/sg_result.log

echo -e "\n${BLUE}=== CDN 配置变更 ===${NC}"
grep "风险等级\|场景描述" test_results/cdn_result.log

# 如果运行了Python测试模块，显示其结果
if [ "$AI_SERVICE_RUNNING" = true ] && [ "$LIME_SERVICE_RUNNING" = true ]; then
    echo -e "\n${BLUE}=== 云资源变更测试 ===${NC}"
    grep "验证" test_results/cloud_changes_test.log | grep -v "开始"
fi

echo -e "\n${BLUE}====================================${NC}"
echo -e "${GREEN}测试完成! 结果已保存到test_results目录${NC}"
echo -e "${BLUE}====================================${NC}"