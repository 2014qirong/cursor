# 腾讯云原生API网关测试用例

基于腾讯云原生API网关文档生成的测试变更用例，用于验证Git智能检测系统的风险识别能力。

## 📋 项目概述

本项目根据[腾讯云原生API网关文档](https://cloud.tencent.com/document/product/1364/72495)生成了一系列测试用例，涵盖了API网关部署、配置、安全策略等多个方面的变更场景。

## 🏗️ 文件结构

```
.
├── terraform/
│   └── tencent_api_gateway.tf          # Terraform基础设施配置
├── k8s/
│   └── tencent-api-gateway-deployment.yaml  # Kubernetes部署配置
├── config/
│   └── api-gateway-config.yaml         # API网关服务配置
├── test_tencent_api_gateway.py          # 测试用例生成器
├── push_to_gitlab.py                   # GitLab推送脚本
└── README_API_GATEWAY_TESTS.md          # 本文档
```

## 🧪 测试用例类型

### 1. 基础设施变更 (Infrastructure Changes)

#### Terraform配置变更
- **文件**: `terraform/tencent_api_gateway.tf`
- **风险等级**: High
- **场景**: VPC网络配置、负载均衡器设置、安全组规则
- **关键变更**:
  - VPC CIDR块修改
  - CLB配置调整
  - 安全组规则变更
  - CAM角色权限修改

#### Kubernetes部署变更
- **文件**: `k8s/tencent-api-gateway-deployment.yaml`
- **风险等级**: High
- **场景**: Kong网关容器化部署配置
- **关键变更**:
  - 副本数量调整
  - 资源限制修改
  - 环境变量配置
  - 健康检查参数

### 2. 服务配置变更 (Service Configuration)

#### API网关配置
- **文件**: `config/api-gateway-config.yaml`
- **风险等级**: Medium-High
- **场景**: 路由规则、插件配置、负载均衡
- **关键变更**:
  - 服务路由规则
  - 限流策略调整
  - JWT认证配置
  - CORS策略修改

### 3. 安全策略变更 (Security Policy Changes)

#### 认证和授权
- **风险等级**: Critical
- **场景**: JWT密钥轮换、SSL证书更新
- **关键变更**:
  - JWT密钥更新
  - SSL证书配置
  - IP访问控制
  - 安全组规则

#### 数据库配置
- **风险等级**: High
- **场景**: 数据库连接配置、密码轮换
- **关键变更**:
  - 数据库连接字符串
  - 用户名密码配置
  - 连接池参数

### 4. 监控和日志配置 (Monitoring & Logging)

#### 日志收集
- **风险等级**: Medium
- **场景**: CLS日志服务配置、Prometheus监控
- **关键变更**:
  - 日志主题配置
  - 监控指标设置
  - 告警规则调整

## 🚀 使用方法

### 1. 环境准备

```bash
# 安装依赖
pip install requests

# 设置GitLab环境变量
export GITLAB_URL='https://gitlab.example.com'
export GITLAB_PROJECT_ID='123'
export GITLAB_ACCESS_TOKEN='glpat-xxxxxxxxxxxxxxxxxxxx'
```

### 2. 生成测试用例

```bash
# 运行测试用例生成器
python test_tencent_api_gateway.py
```

### 3. 推送到GitLab

```bash
# 推送所有测试用例到GitLab
python push_to_gitlab.py
```

### 4. 手动推送单个用例

```python
from test_tencent_api_gateway import TencentAPIGatewayTestGenerator
from push_to_gitlab import GitLabPusher

# 初始化
generator = TencentAPIGatewayTestGenerator(gitlab_url, project_id, token)
pusher = GitLabPusher(gitlab_url, project_id, token)

# 生成并推送特定测试用例
test_cases = generator.generate_test_cases()
high_risk_cases = [case for case in test_cases if case['risk_level'] == 'high']

for case in high_risk_cases:
    pusher.push_test_case(case)
```

## 📊 测试用例详情

### 高风险用例 (High Risk)

| 用例名称 | 文件路径 | 风险点 | 影响范围 |
|---------|----------|--------|----------|
| 生产环境核心配置变更 | `terraform/production/` | 网络架构变更 | 全局服务 |
| 数据库配置变更 | `k8s/deployment.yaml` | 数据持久化 | 数据完整性 |
| 负载均衡器配置 | `terraform/clb.tf` | 流量分发 | 服务可用性 |
| 网络策略变更 | `k8s/network-policy.yaml` | 网络隔离 | 安全边界 |

### 关键风险用例 (Critical Risk)

| 用例名称 | 文件路径 | 风险点 | 影响范围 |
|---------|----------|--------|----------|
| 密钥和证书管理 | `config/secrets.yaml` | 认证凭据 | 系统安全 |
| SSL证书配置 | `terraform/certificate.tf` | 加密通信 | 数据传输 |
| JWT密钥轮换 | `config/jwt-config.yaml` | 身份验证 | 用户访问 |

### 中等风险用例 (Medium Risk)

| 用例名称 | 文件路径 | 风险点 | 影响范围 |
|---------|----------|--------|----------|
| 插件配置变更 | `config/plugins.yaml` | 功能特性 | 业务逻辑 |
| 监控配置调整 | `config/monitoring.yaml` | 可观测性 | 运维监控 |
| 日志配置变更 | `config/logging.yaml` | 日志收集 | 问题排查 |

## 🔍 风险识别要点

### 1. 基础设施层面
- **网络配置变更**: CIDR块修改可能导致网络隔离问题
- **资源限制调整**: CPU/内存限制变更影响服务性能
- **副本数量变更**: 影响服务高可用性

### 2. 安全层面
- **认证配置变更**: JWT密钥、SSL证书等敏感配置
- **访问控制**: IP白名单、安全组规则变更
- **权限管理**: CAM角色和策略配置

### 3. 服务层面
- **路由规则变更**: 可能导致流量路由错误
- **限流策略调整**: 影响服务保护机制
- **健康检查配置**: 影响服务发现和负载均衡

### 4. 数据层面
- **数据库配置**: 连接参数、认证信息变更
- **数据持久化**: 存储卷配置变更
- **备份策略**: 数据保护机制调整

## 🎯 AI风险分析预期

### 高风险识别场景
1. **生产环境标识**: 包含`production`、`prod`关键字的文件路径
2. **敏感配置变更**: 密码、密钥、证书等敏感信息修改
3. **核心资源调整**: 副本数量大幅减少、资源限制大幅降低
4. **网络架构变更**: VPC、子网、安全组等网络配置修改

### 中等风险识别场景
1. **插件配置调整**: 限流、认证等插件参数修改
2. **监控配置变更**: 监控指标、告警规则调整
3. **日志配置修改**: 日志级别、输出格式变更

### 低风险识别场景
1. **文档更新**: README、注释等文档性变更
2. **测试配置**: 测试环境相关配置调整
3. **非关键参数**: 超时时间、重试次数等参数微调

## 🔧 自定义配置

### 修改测试用例

编辑 `test_tencent_api_gateway.py` 文件中的测试用例生成方法：

```python
def _generate_custom_test_case(self) -> Dict[str, Any]:
    return {
        "test_name": "自定义测试用例",
        "risk_level": "high",
        "description": "自定义的风险场景描述",
        "files_changed": [
            "path/to/your/config.yaml"
        ],
        "diff_content": """
--- a/path/to/your/config.yaml
+++ b/path/to/your/config.yaml
@@ -10,7 +10,7 @@
-  old_value: original
+  new_value: modified
        """,
        "commit_message": "feat: 自定义配置变更",
        "author": "your-team",
        "branch": "feature/custom-change"
    }
```

### 配置GitLab推送

修改 `push_to_gitlab.py` 中的推送逻辑：

```python
# 自定义分支命名规则
branch_name = f"test-{test_case['risk_level']}-{int(time.time())}"

# 自定义合并请求模板
description_template = f"""
## 🧪 测试用例: {test_case['test_name']}

### 📋 基本信息
- **风险等级**: {test_case['risk_level']}
- **变更类型**: API网关配置
- **影响范围**: {test_case.get('impact_scope', '待评估')}

### 📝 变更描述
{test_case['description']}

### 🔍 风险分析要点
- 检查是否正确识别风险等级
- 验证AI模型对腾讯云API网关配置的理解
- 确认LIME解释的合理性
"""
```

## 📈 监控和验证

### 1. 推送状态监控

```bash
# 查看推送日志
tail -f gitlab_push.log

# 检查GitLab项目状态
curl -H "PRIVATE-TOKEN: $GITLAB_ACCESS_TOKEN" \
     "$GITLAB_URL/api/v4/projects/$PROJECT_ID/merge_requests"
```

### 2. AI分析结果验证

推送完成后，可以通过以下方式验证AI分析结果：

1. **查看变更列表**: 访问后端API `/api/v1/changes`
2. **检查风险评估**: 确认AI模型的风险等级判断
3. **验证LIME解释**: 查看模型决策的可解释性分析
4. **测试OPA决策**: 验证规则引擎的决策结果

### 3. 性能指标

监控以下关键指标：
- **推送成功率**: 目标 > 95%
- **AI分析准确率**: 高风险用例识别率 > 90%
- **响应时间**: 单个变更分析时间 < 30秒
- **系统可用性**: 服务正常运行时间 > 99.9%

## 🚨 注意事项

### 安全考虑
1. **敏感信息**: 测试用例中的密钥、密码均为示例，请勿在生产环境使用
2. **访问权限**: 确保GitLab访问令牌具有适当的权限范围
3. **网络安全**: 推送过程中注意网络安全和数据传输加密

### 最佳实践
1. **分批推送**: 避免一次性推送大量测试用例造成系统负载
2. **版本控制**: 保持测试用例的版本管理和变更记录
3. **定期更新**: 根据腾讯云API网关的更新及时调整测试用例

### 故障排除

#### 常见问题

1. **推送失败**
   ```bash
   # 检查网络连接
   curl -I $GITLAB_URL
   
   # 验证访问令牌
   curl -H "PRIVATE-TOKEN: $GITLAB_ACCESS_TOKEN" \
        "$GITLAB_URL/api/v4/user"
   ```

2. **分支创建失败**
   ```bash
   # 检查分支命名规范
   # 确保分支名称符合GitLab规范
   ```

3. **文件编码问题**
   ```python
   # 确保文件以UTF-8编码保存
   with open(file_path, 'r', encoding='utf-8') as f:
       content = f.read()
   ```

## 📞 支持和反馈

如有问题或建议，请通过以下方式联系：

- **项目Issues**: 在GitLab项目中创建Issue
- **技术文档**: 参考腾讯云官方文档
- **社区支持**: 腾讯云开发者社区

---

*本测试用例集基于腾讯云原生API网关官方文档生成，用于验证Git智能检测系统的AI风险分析能力。*