from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import requests
import json
import numpy as np
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import re
from enhanced_model import EnhancedRiskModel

# 新增：云平台变更预处理模块
# 尝试导入模块
try:
    from cloud_change_processor import preprocess_infrastructure_change, match_change_with_knowledge_base
except ImportError:
    # 将模块定义内联到此文件中
    import difflib
    from typing import Dict, List, Tuple, Optional, Any
    
    # 变更类型关键字匹配
    CLOUD_KEYWORDS = {
        "AWS": ["aws", "amazon", "ec2", "s3", "rds", "eks", "iam", "dynamodb", "lambda", "cloudfront", "route53"],
        "AliCloud": ["aliyun", "alibaba", "alicloud", "oss", "ecs", "rds", "acr", "ack", "ram"],
        "TencentCloud": ["tencent", "qcloud", "cos", "cvm", "tke", "tcr", "cls", "cam", "clb"]
    }

    RESOURCE_KEYWORDS = {
        "K8s": ["kubernetes", "k8s", "pod", "deployment", "service", "ingress", "configmap", "kind:", "apiVersion:"],
        "Terraform": ["terraform", "provider ", "resource ", "module ", ".tf", "tf plan", "tf apply"],
        "Network": ["vpc", "subnet", "cidr", "route table", "security group", "acl", "网络", "路由"],
        "Storage": ["存储", "s3", "oss", "cos", "bucket", "对象存储"],
        "Database": ["rds", "database", "数据库", "mysql", "sql", "redis"],
        "Compute": ["ec2", "ecs", "cvm", "vm", "instance", "eks", "ack", "tke", "container"],
        "IAM": ["iam", "ram", "cam", "role", "policy", "permission", "权限"]
    }

    def preprocess_infrastructure_change(content: str) -> Tuple[str, str]:
        """预处理基础设施变更内容，识别变更类型并提取关键信息"""
        content_lower = content.lower()
        
        # 识别云平台
        cloud_platforms = []
        for platform, keywords in CLOUD_KEYWORDS.items():
            if any(keyword in content_lower for keyword in keywords):
                cloud_platforms.append(platform)
        
        # 识别资源类型
        resource_types = []
        for res_type, keywords in RESOURCE_KEYWORDS.items():
            if any(keyword in content_lower for keyword in keywords):
                resource_types.append(res_type)
        
        # 基本类型识别
        if "k8s" in resource_types or (("apiVersion:" in content) and ("kind:" in content)):
            if "ingress" in content_lower:
                for platform in cloud_platforms:
                    return f"{platform}_K8S_INGRESS_UPDATE", content
            
        # IAM 相关变更
        if "iam" in resource_types and cloud_platforms:
            if ("create" in content_lower and "user" in content_lower):
                if any(keyword in content_lower for keyword in ["admin", "administrator", "root", "*:*:*"]):
                    return "CLOUD_IAM_USER_CREATE_OVER_PRIVILEGE", content
        
        # 通用类型
        if cloud_platforms:
            platform = cloud_platforms[0]
            for res in resource_types:
                return f"{platform}_{res.upper()}_CHANGE", content
        
        return "", content
    
    def match_change_with_knowledge_base(change_type: str, content: str, kb: Dict) -> Optional[Dict[str, Any]]:
        """将预处理后的变更与知识库进行匹配"""
        if not change_type:
            return None
        
        content_lower = content.lower()
        change_items = kb.get("change_items", [])
        best_match = None
        best_score = 0
        
        # 精确匹配
        for item in change_items:
            if item.get("type") == change_type:
                return item
        
        # 部分匹配
        change_type_parts = change_type.split("_")
        for item in change_items:
            item_type = item.get("type", "")
            
            # 计算匹配分数
            match_score = 0
            
            # 类型匹配
            for part in change_type_parts:
                if part in item_type:
                    match_score += 1
            
            if match_score > best_score:
                best_score = match_score
                best_match = item
        
        if best_score >= 1:
            return best_match
        
        return None

app = FastAPI()

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/risk_clf.pkl')

# InfluxDB 配置从环境变量获取
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw==")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "risk_assessment")

# 加载云平台变更风险知识库
KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cloud_change_risk_assessment_kb.json'))

# 加载知识库
print("加载云平台变更风险知识库...")
try:
    with open(KNOWLEDGE_BASE_PATH, 'r') as f:
        CLOUD_KNOWLEDGE_BASE = json.load(f)
    print(f"知识库加载成功，包含 {len(CLOUD_KNOWLEDGE_BASE.get('change_items', []))} 条变更记录")
except Exception as e:
    print(f"加载知识库失败: {e}")
    CLOUD_KNOWLEDGE_BASE = {"change_items": []}

# 风险描述模板
RISK_DESCRIPTIONS = {
    "高危": {
        "os.system": {
            "description": "检测到潜在的命令注入风险。使用 os.system() 直接执行命令可能导致远程代码执行漏洞。",
            "suggestions": [
                "使用参数化的安全API替代 os.system()",
                "实施命令白名单机制",
                "对输入进行严格的过滤和验证"
            ]
        },
        "eval": {
            "description": "检测到潜在的代码注入风险。使用 eval() 执行动态代码可能导致远程代码执行漏洞。",
            "suggestions": [
                "避免使用 eval() 函数",
                "使用更安全的替代方案，如 ast.literal_eval()",
                "实施输入验证和过滤"
            ]
        },
        "default": {
            "description": "检测到潜在的安全风险。代码中可能存在安全漏洞。",
            "suggestions": [
                "进行代码安全审计",
                "遵循安全编码规范",
                "添加必要的安全控制"
            ]
        }
    },
    "低危": {
        "default": {
            "description": "未检测到明显的安全风险。",
            "suggestions": [
                "定期进行代码审查",
                "保持安全意识",
                "遵循最佳实践"
            ]
        }
    }
}

# 加载模型
print("加载模型...")
base_model = joblib.load(MODEL_PATH)
knowledge_base_path = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')
model = EnhancedRiskModel(base_model, knowledge_base_path)
print("模型加载成功")

# 初始化 InfluxDB 客户端
client = influxdb_client.InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)
write_api = client.write_api(write_options=SYNCHRONOUS)
print("InfluxDB client initialized.")

class DiffRequest(BaseModel):
    diff_content: str

class CodeInput(BaseModel):
    code: str

class GitLabWebhookPayload(BaseModel):
    object_kind: str
    event_name: str
    before: str
    after: str
    ref: str
    checkout_sha: str
    message: str
    user_id: int
    user_name: str
    user_username: str
    user_email: str
    user_avatar: str
    project_id: int
    project: dict
    commits: list
    total_commits_count: int
    repository: dict

def get_risk_description(diff_content: str, risk_level: str) -> dict:
    """
    根据代码内容和风险等级生成风险描述
    """
    if risk_level == "高危":
        # 检查特定的风险模式
        if re.search(r'os\.system\s*\(', diff_content):
            return RISK_DESCRIPTIONS["高危"]["os.system"]
        elif re.search(r'eval\s*\(', diff_content):
            return RISK_DESCRIPTIONS["高危"]["eval"]
        return RISK_DESCRIPTIONS["高危"]["default"]
    return RISK_DESCRIPTIONS["低危"]["default"]

@app.on_event("startup")
async def startup_event():
    global model, client, write_api
    try:
        model = joblib.load(MODEL_PATH)
        print("模型加载成功")
    except FileNotFoundError:
        print(f"未找到模型文件: {MODEL_PATH}")
        raise FileNotFoundError(f"未找到模型文件: {MODEL_PATH}")

    # 重新初始化 InfluxDB 客户端 (如果在全局初始化时失败)
    if client is None or write_api is None:
        try:
            client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            print("InfluxDB client initialized during startup.")
        except Exception as e:
            print(f"Error initializing InfluxDB client during startup: {e}")

@app.post("/predict")
async def predict(input: CodeInput):
    try:
        print(f"接收到输入，长度: {len(input.code)}")
        
        # 直接检测，如果存在kind: NodePool就强制识别为腾讯云TKE节点池变更
        if "kind: NodePool" in input.code or "kind:NodePool" in input.code:
            print("强制匹配: 发现kind: NodePool，直接返回TENCENTCLOUD_TKE_NODE_POOL_UPDATE")
            change_type = "TENCENTCLOUD_TKE_NODE_POOL_UPDATE"
            preprocessed_input = input.code
        # 直接检测阿里云OSS存储桶权限变更
        elif (("阿里云OSS" in input.code or "aliyun oss" in input.code.lower()) and 
              ("bucket" in input.code.lower() or "存储桶" in input.code) and 
              ("acl" in input.code.lower() or "权限" in input.code or "public-read" in input.code.lower())):
            print("强制匹配: 发现阿里云OSS权限变更，直接返回CLOUD_OBJECT_STORAGE_BUCKET_POLICY_UPDATE")
            change_type = "CLOUD_OBJECT_STORAGE_BUCKET_POLICY_UPDATE"
            preprocessed_input = input.code
        else:
            # 对输入进行预处理，识别变更类型和关键信息
            change_type, preprocessed_input = preprocess_infrastructure_change(input.code)
        
        print(f"预处理完成，变更类型: {change_type}")
        
        # 测试直接返回处理结果
        if input.code.startswith("# TEST_ECHO"):
            return {
                "change_type": change_type,
                "preprocessed": preprocessed_input[:200] + "...(截断)" if len(preprocessed_input) > 200 else preprocessed_input,
                "cloud_platforms": [p for p, keywords in CLOUD_KEYWORDS.items() 
                                   if any(k in input.code.lower() for k in keywords)],
                "resource_types": [r for r, keywords in RESOURCE_KEYWORDS.items() 
                                  if any(k in input.code.lower() for k in keywords)]
            }
        
        # 根据变更类型和内容，与知识库进行匹配
        if change_type:
            risk_item = match_change_with_knowledge_base(change_type, preprocessed_input, CLOUD_KNOWLEDGE_BASE)
            
            if risk_item:
                print(f"匹配到知识库项: {risk_item.get('type')}")
                # 直接使用知识库中的风险评估结果
                result = {
                    'probability': convert_risk_level_to_probability(risk_item.get('risk_level', 'Medium')),
                    'risk_level': risk_item.get('risk_level', 'Medium'),
                    'matched_pattern': {
                        'content': risk_item.get('description', ''),
                        'source': "云变更风险知识库",
                        'key_metrics_to_monitor': risk_item.get('key_metrics_to_monitor', []),
                        'potential_impacts': risk_item.get('potential_impacts', []),
                        'mitigation_strategies': risk_item.get('mitigation_strategies', [])
                    },
                    'suggested_solution': {
                        'content': "\n".join(risk_item.get('pre_change_checklist', [])),
                        'source': "云变更风险最佳实践"
                    }
                }
            else:
                print("未匹配到知识库项，尝试使用模型预测")
                # 未匹配到知识库项，尝试使用模型预测
                try:
                    result = model.predict(preprocessed_input)
                except Exception as e:
                    print(f"模型预测错误: {str(e)}")
                    # 使用默认结果
                    result = {
                        'probability': 0.5,
                        'risk_level': "中风险",
                        'matched_pattern': {
                            'content': f"未能精确匹配到已知风险模式，但检测到云资源变更 ({change_type})",
                            'source': "云变更风险通用检测",
                            'key_metrics_to_monitor': ["资源CPU利用率", "内存利用率", "请求成功率"],
                            'potential_impacts': ["服务可能出现短暂不可用", "性能可能受到影响"],
                            'mitigation_strategies': ["预先备份相关配置", "准备回滚方案", "执行充分测试"]
                        }
                    }
        else:
            # 非云平台变更或无法识别的变更，使用原有模型
            print("使用基础模型进行预测")
            result = model.predict(input.code)
        
        # 写入 InfluxDB
        point = influxdb_client.Point("risk_assessment") \
            .field("probability", result['probability']) \
            .field("risk_level", result['risk_level'])
        
        if 'matched_pattern' in result:
            point = point.field("matched_pattern", result['matched_pattern']['content']) \
                .field("pattern_source", result['matched_pattern']['source'])
            # 新增结构化风险信息写入
            for field in [
                'key_metrics_to_monitor',
                'potential_impacts',
                'mitigation_strategies'
            ]:
                if field in result['matched_pattern']:
                    # 以字符串形式写入，便于Grafana表格展示
                    value = result['matched_pattern'][field]
                    if isinstance(value, list):
                        value = '\n'.join(value)
                    point = point.field(field, value)
        
        if 'suggested_solution' in result:
            point = point.field("solution", result['suggested_solution']['content']) \
                .field("solution_source", result['suggested_solution']['source'])
        
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"写入 InfluxDB 成功: probability={result['probability']}")
        
        return result
    except Exception as e:
        print(f"预测错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 辅助函数：风险等级转换为概率值
def convert_risk_level_to_probability(risk_level):
    risk_mapping = {
        'Critical': 0.95,
        'High': 0.85,
        'Medium': 0.65,
        'Low': 0.35
    }
    return risk_mapping.get(risk_level, 0.5)

# 辅助函数：从 GitLab API 获取 commit diff
async def get_commit_diff(project_id: int, commit_sha: str, gitlab_token: str = None) -> str:
    """
    从 GitLab API 获取指定 commit 的 diff 内容
    """
    try:
        # 如果没有提供 GitLab token，尝试从环境变量获取
        if not gitlab_token:
            gitlab_token = os.getenv("GITLAB_TOKEN")
        
        if not gitlab_token:
            print("警告: 未提供 GitLab token，无法获取详细 diff")
            return ""
        
        # GitLab API URL (假设是 GitLab.com，如果是私有实例需要修改)
        gitlab_url = os.getenv("GITLAB_URL", "https://gitlab.com")
        api_url = f"{gitlab_url}/api/v4/projects/{project_id}/repository/commits/{commit_sha}/diff"
        
        headers = {
            "Authorization": f"Bearer {gitlab_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            diffs = response.json()
            # 合并所有文件的 diff 内容
            combined_diff = ""
            for diff in diffs:
                if 'diff' in diff:
                    combined_diff += f"\n--- {diff.get('old_path', 'unknown')}\n"
                    combined_diff += f"+++ {diff.get('new_path', 'unknown')}\n"
                    combined_diff += diff['diff'] + "\n"
            return combined_diff
        else:
            print(f"获取 diff 失败: HTTP {response.status_code}")
            return ""
    except Exception as e:
        print(f"获取 commit diff 时出错: {str(e)}")
        return ""

@app.post("/gitlab-webhook")
async def gitlab_webhook(payload: GitLabWebhookPayload):
    """
    处理 GitLab Webhook 请求，解析 Push Event 并进行风险评估
    """
    try:
        print(f"收到 GitLab Webhook: {payload.object_kind} - {payload.event_name}")
        
        # 只处理 push 事件
        if payload.object_kind != "push":
            return {"message": f"忽略非 push 事件: {payload.object_kind}", "status": "ignored"}
        
        # 提取项目和提交信息
        project_id = payload.project_id
        project_name = payload.project.get("name", "unknown") if payload.project else "unknown"
        commits = payload.commits or []
        
        print(f"处理项目 {project_name} (ID: {project_id}) 的 {len(commits)} 个提交")
        
        # 收集所有变更内容
        all_changes = []
        risk_results = []
        
        for commit in commits:
            commit_id = commit.get("id", "")
            commit_message = commit.get("message", "")
            commit_author = commit.get("author", {}).get("name", "unknown")
            
            print(f"处理提交: {commit_id[:8]} by {commit_author}")
            
            # 尝试从 payload 中获取文件变更信息
            added_files = commit.get("added", [])
            modified_files = commit.get("modified", [])
            removed_files = commit.get("removed", [])
            
            # 构建变更摘要
            change_summary = f"Commit: {commit_id[:8]}\n"
            change_summary += f"Author: {commit_author}\n"
            change_summary += f"Message: {commit_message}\n"
            
            if added_files:
                change_summary += f"Added files: {', '.join(added_files)}\n"
            if modified_files:
                change_summary += f"Modified files: {', '.join(modified_files)}\n"
            if removed_files:
                change_summary += f"Removed files: {', '.join(removed_files)}\n"
            
            # 尝试获取详细的 diff 内容
            diff_content = await get_commit_diff(project_id, commit_id)
            
            if diff_content:
                change_summary += f"\nDiff content:\n{diff_content}"
            else:
                # 如果无法获取详细 diff，使用文件列表作为分析内容
                change_summary += f"\nFile changes summary: {len(added_files)} added, {len(modified_files)} modified, {len(removed_files)} removed"
            
            all_changes.append(change_summary)
            
            # 对每个提交进行风险评估
            try:
                # 使用现有的预测接口
                code_input = CodeInput(code=change_summary)
                
                # 直接检测，如果存在kind: NodePool就强制识别为腾讯云TKE节点池变更
                if "kind: NodePool" in change_summary or "kind:NodePool" in change_summary:
                    print("强制匹配: 发现kind: NodePool，直接返回TENCENTCLOUD_TKE_NODE_POOL_UPDATE")
                    change_type = "TENCENTCLOUD_TKE_NODE_POOL_UPDATE"
                    preprocessed_input = change_summary
                # 直接检测阿里云OSS存储桶权限变更
                elif (("阿里云OSS" in change_summary or "aliyun oss" in change_summary.lower()) and 
                      ("bucket" in change_summary.lower() or "存储桶" in change_summary) and 
                      ("acl" in change_summary.lower() or "权限" in change_summary or "public-read" in change_summary.lower())):
                    print("强制匹配: 发现阿里云OSS权限变更，直接返回CLOUD_OBJECT_STORAGE_BUCKET_POLICY_UPDATE")
                    change_type = "CLOUD_OBJECT_STORAGE_BUCKET_POLICY_UPDATE"
                    preprocessed_input = change_summary
                else:
                    # 对输入进行预处理，识别变更类型和关键信息
                    change_type, preprocessed_input = preprocess_infrastructure_change(change_summary)
                
                print(f"预处理完成，变更类型: {change_type}")
                
                # 根据变更类型和内容，与知识库进行匹配
                if change_type:
                    risk_item = match_change_with_knowledge_base(change_type, preprocessed_input, CLOUD_KNOWLEDGE_BASE)
                    
                    if risk_item:
                        print(f"匹配到知识库项: {risk_item.get('type')}")
                        # 直接使用知识库中的风险评估结果
                        result = {
                            'commit_id': commit_id,
                            'commit_author': commit_author,
                            'commit_message': commit_message,
                            'probability': convert_risk_level_to_probability(risk_item.get('risk_level', 'Medium')),
                            'risk_level': risk_item.get('risk_level', 'Medium'),
                            'change_type': change_type,
                            'matched_pattern': {
                                'content': risk_item.get('description', ''),
                                'source': "云变更风险知识库",
                                'key_metrics_to_monitor': risk_item.get('key_metrics_to_monitor', []),
                                'potential_impacts': risk_item.get('potential_impacts', []),
                                'mitigation_strategies': risk_item.get('mitigation_strategies', [])
                            },
                            'suggested_solution': {
                                'content': "\n".join(risk_item.get('pre_change_checklist', [])),
                                'source': "云变更风险最佳实践"
                            }
                        }
                    else:
                        print("未匹配到知识库项，使用默认风险评估")
                        # 未匹配到知识库项，使用默认结果
                        result = {
                            'commit_id': commit_id,
                            'commit_author': commit_author,
                            'commit_message': commit_message,
                            'probability': 0.5,
                            'risk_level': "中风险",
                            'change_type': change_type,
                            'matched_pattern': {
                                'content': f"未能精确匹配到已知风险模式，但检测到云资源变更 ({change_type})",
                                'source': "云变更风险通用检测",
                                'key_metrics_to_monitor': ["资源CPU利用率", "内存利用率", "请求成功率"],
                                'potential_impacts': ["服务可能出现短暂不可用", "性能可能受到影响"],
                                'mitigation_strategies': ["预先备份相关配置", "准备回滚方案", "执行充分测试"]
                            }
                        }
                else:
                    # 非云平台变更或无法识别的变更
                    print("无法识别变更类型，使用低风险评估")
                    result = {
                        'commit_id': commit_id,
                        'commit_author': commit_author,
                        'commit_message': commit_message,
                        'probability': 0.3,
                        'risk_level': "低风险",
                        'change_type': "UNKNOWN",
                        'matched_pattern': {
                            'content': "未识别到特定的云资源变更模式",
                            'source': "通用代码变更检测",
                            'key_metrics_to_monitor': ["基本系统指标"],
                            'potential_impacts': ["影响较小"],
                            'mitigation_strategies': ["常规代码审查"]
                        }
                    }
                
                risk_results.append(result)
                
                # 写入 InfluxDB
                point = influxdb_client.Point("gitlab_webhook_risk_assessment") \
                    .tag("project_id", str(project_id)) \
                    .tag("project_name", project_name) \
                    .tag("commit_id", commit_id) \
                    .tag("commit_author", commit_author) \
                    .tag("change_type", change_type or "UNKNOWN") \
                    .field("probability", result['probability']) \
                    .field("risk_level", result['risk_level']) \
                    .field("commit_message", commit_message)
                
                if 'matched_pattern' in result:
                    point = point.field("matched_pattern", result['matched_pattern']['content']) \
                        .field("pattern_source", result['matched_pattern']['source'])
                
                write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
                print(f"GitLab Webhook 风险评估写入 InfluxDB 成功: commit={commit_id[:8]}, risk={result['risk_level']}")
                
            except Exception as e:
                print(f"处理提交 {commit_id} 时出错: {str(e)}")
                # 添加错误记录
                error_result = {
                    'commit_id': commit_id,
                    'commit_author': commit_author,
                    'commit_message': commit_message,
                    'error': str(e),
                    'probability': 0.0,
                    'risk_level': "处理失败"
                }
                risk_results.append(error_result)
        
        # 返回汇总结果
        return {
            "message": "GitLab Webhook 处理完成",
            "status": "success",
            "project_id": project_id,
            "project_name": project_name,
            "total_commits": len(commits),
            "processed_commits": len(risk_results),
            "risk_assessments": risk_results
        }
        
    except Exception as e:
        print(f"GitLab Webhook 处理错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理 GitLab Webhook 时出错: {str(e)}")

@app.post("/explain")
async def explain(input: CodeInput):
    try:
        # 获取预测解释
        explanation = model.explain(input.code)
        
        # 写入 InfluxDB
        point = influxdb_client.Point("risk_assessment") \
            .field("explanation", str(explanation))
        
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"写入 InfluxDB 成功: explanation={str(explanation)}")
        
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """
    健康检查端点
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)