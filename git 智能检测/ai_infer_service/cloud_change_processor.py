"""
云平台基础设施变更预处理模块
用于识别变更类型、提取关键信息，并与知识库进行匹配
支持：
- AWS、阿里云、腾讯云等云平台
- Kubernetes YAML
- Terraform
- ArgoCD
- 云 API/控制台操作描述
"""

import re
import json
import difflib
from typing import Dict, List, Tuple, Optional, Any

# 变更类型关键字匹配
CLOUD_KEYWORDS = {
    "AWS": ["aws", "amazon", "ec2", "s3", "rds", "eks", "iam", "dynamodb", "lambda", "cloudfront", "route53", "msk", "global accelerator"],
    "AliCloud": ["aliyun", "alibaba", "alicloud", "oss", "ecs", "rds", "polardb", "acr", "ack", "ram", "cdn", "cen"],
    "TencentCloud": ["tencent", "qcloud", "cos", "cvm", "tke", "tcr", "cls", "cam", "clb", "ccn", "ckafka"]
}

RESOURCE_KEYWORDS = {
    "K8s": ["kubernetes", "k8s", "pod", "deployment", "service", "ingress", "configmap", "secret", "namespace", "kind:", "apiVersion:", "kubectl"],
    "Terraform": ["terraform", "provider ", "resource ", "module ", "output ", "variable ", ".tf", "tf plan", "tf apply"],
    "ArgoCD": ["argocd", "argo cd", "argo", "sync", "application.yaml", "app of apps", "helm chart"],
    "CloudAPI": ["api", "sdk", "cli", "aws-cli", "awscli", "aliyun cli", "tencentcloud-cli", "tencentcloud cli"],
    "Network": ["vpc", "subnet", "cidr", "route table", "security group", "acl", "firewall", "nat", "网络", "路由", "安全组", "防火墙"],
    "Storage": ["存储", "s3", "oss", "cos", "bucket", "对象存储", "块存储", "文件存储", "block", "file", "disk", "volume"],
    "Database": ["rds", "database", "数据库", "mysql", "postgresql", "mongo", "sql", "nosql", "redis", "elasticache", "memcached"],
    "Compute": ["ec2", "ecs", "cvm", "vm", "instance", "eks", "ack", "tke", "container", "kubernetes", "容器", "虚拟机"],
    "IAM": ["iam", "ram", "cam", "role", "policy", "permission", "权限", "认证", "auth", "鉴权", "aksk", "access key", "secret key"]
}

def preprocess_infrastructure_change(content: str) -> Tuple[str, str]:
    """
    预处理基础设施变更内容，识别变更类型并提取关键信息
    
    Args:
        content: 变更内容文本
        
    Returns:
        Tuple[str, str]: (变更类型, 处理后的文本)
    """
    print("[DEBUG] preprocess_infrastructure_change called!\n前100字符：", content[:100])
    # 只要出现kind: NodePool（不论云平台关键词），直接认定为TKE节点池变更
    if re.search(r"kind:\s*['\"]?nodepool['\"]?", content, re.IGNORECASE):
        print("[DEBUG] 命中NodePool，直接返回TENCENTCLOUD_TKE_NODE_POOL_UPDATE")
        return "TENCENTCLOUD_TKE_NODE_POOL_UPDATE", content

    # 阿里云OSS存储桶权限变更
    if (("阿里云" in content or "alicloud" in content.lower() or "oss" in content.lower()) and 
        ("bucket" in content.lower() or "存储桶" in content) and 
        ("acl" in content.lower() or "权限" in content or "public-read" in content.lower())):
        print("[DEBUG] 命中阿里云OSS权限变更，返回CLOUD_OBJECT_STORAGE_BUCKET_POLICY_UPDATE")
        return "CLOUD_OBJECT_STORAGE_BUCKET_POLICY_UPDATE", content

    content_lower = content.lower()
    
    # 打印诊断信息
    print(f"处理变更内容，长度: {len(content)}")
    
    # 识别云平台
    cloud_platforms = []
    for platform, keywords in CLOUD_KEYWORDS.items():
        if any(keyword in content_lower for keyword in keywords) or any(keyword in content for keyword in keywords if re.search("[\u4e00-\u9fa5]", keyword)):
            cloud_platforms.append(platform)
    
    print(f"识别到的云平台: {cloud_platforms}")
    
    # 识别资源类型
    resource_types = []
    for res_type, keywords in RESOURCE_KEYWORDS.items():
        if any(keyword in content_lower for keyword in keywords) or any(keyword in content for keyword in keywords if re.search("[\u4e00-\u9fa5]", keyword)):
            resource_types.append(res_type)
    
    print(f"识别到的资源类型: {resource_types}")
    
    # 如果是 Kubernetes YAML 格式
    if "k8s" in resource_types or (("apiVersion:" in content_lower) and ("kind:" in content_lower)):
        change_type = _identify_k8s_change(content)
        if change_type:
            return change_type, _extract_kubernetes_changes(content)
    
    # 如果是 Terraform 相关
    if "terraform" in resource_types or (".tf" in content_lower) or ("resource" in content and "{" in content):
        change_type = _identify_terraform_change(content, cloud_platforms)
        if change_type:
            return change_type, _extract_terraform_changes(content)
    
    # 网络相关变更
    if "network" in resource_types and cloud_platforms:
        if "route" in content_lower and "table" in content_lower:
            if "aws" in cloud_platforms:
                return "AWS_VPC_ROUTER_ROUTE_UPDATE", content
            elif "alicloud" in [p.lower() for p in cloud_platforms]:
                return "ALICLOUD_VPC_ROUTER_ROUTE_UPDATE", content
            elif "tencentcloud" in [p.lower() for p in cloud_platforms]:
                return "TENCENTCLOUD_VPC_ROUTER_ROUTE_UPDATE", content
    
    # IAM 相关变更
    if "iam" in resource_types and cloud_platforms:
        if ("create" in content_lower and "user" in content_lower) or ("new" in content_lower and "user" in content_lower):
            if any(keyword in content_lower for keyword in ["admin", "administrator", "root", "full", "all", "*:*:*"]):
                return "CLOUD_IAM_USER_CREATE_OVER_PRIVILEGE", content
        if "key" in content_lower and any(keyword in content_lower for keyword in ["access", "ak", "sk", "secret"]):
            if any(keyword in content_lower for keyword in ["admin", "administrator", "root", "full", "all", "*:*:*"]):
                return "CLOUD_AKSK_CREATE_OVER_PRIVILEGE", content
    
    # 如果没有明确识别出类型但有云平台关键词，给出通用类型
    if cloud_platforms:
        platform = cloud_platforms[0]
        if "network" in resource_types:
            return f"{platform}_NETWORK_CHANGE", content
        elif "storage" in resource_types:
            return f"{platform}_STORAGE_CHANGE", content
        elif "database" in resource_types:
            return f"{platform}_DATABASE_CHANGE", content
        elif "compute" in resource_types:
            return f"{platform}_COMPUTE_CHANGE", content
        else:
            return f"{platform}_GENERAL_CHANGE", content
    
    # 无法识别的情况
    return "", content

def _identify_k8s_change(content: str) -> str:
    """识别 Kubernetes 变更类型"""
    content_lower = content.lower()
    
    # 提取 kind 和 metadata.name
    kind_match = re.search(r"kind:\s*['\"]?([^'\"\n]+)['\"]?", content)
    name_match = re.search(r"name:\s*['\"]?([^'\"\n]+)['\"]?", content)
    
    kind = kind_match.group(1).lower() if kind_match else ""
    print(f"K8s资源kind: {kind}")
    
    # NodePool 变更 (腾讯云TKE)
    if (kind == "nodepool" or "nodepool" in content_lower) and ("tke" in content_lower or "tencent" in content_lower):
        print("通过kind=NodePool匹配到腾讯云TKE节点池变更")
        return "TENCENTCLOUD_TKE_NODE_POOL_UPDATE"
    
    # Ingress 变更
    if kind == "ingress" or "ingress" in content_lower:
        if "aws" in content_lower:
            return "AWS_INGRESS_UPDATE"
        elif "alicloud" in content_lower or "aliyun" in content_lower:
            return "ALICLOUD_ACK_INGRESS_UPDATE"
        elif "tencent" in content_lower:
            return "TENCENTCLOUD_K8S_INGRESS_UPDATE_HELM_ARGOCD"
        else:
            return "K8S_INGRESS_UPDATE"
    
    # Deployment 变更
    if kind == "deployment" or "deployment" in content_lower:
        if "replicas" in content_lower:
            if "tencent" in content_lower:
                return "TENCENTCLOUD_TKE_POD_REPLICAS_UPDATE_ARGOCD"
            else:
                return "K8S_DEPLOYMENT_REPLICAS_UPDATE"
    
    return ""

def _identify_terraform_change(content: str, cloud_platforms: List[str]) -> str:
    """识别 Terraform 变更类型"""
    content_lower = content.lower()
    
    # 根据云平台和资源类型识别
    for platform in cloud_platforms:
        platform_lower = platform.lower()
        
        # 路由表变更
        if "route" in content_lower and "table" in content_lower:
            return f"{platform}_ROUTE53_RECORD_UPDATE_TF"
        
        # 安全组变更
        if ("security" in content_lower and "group" in content_lower) or "sg_rule" in content_lower:
            if platform_lower == "alicloud":
                return "ALICLOUD_ECS_SG_RULE_CHANGE_TF"
        
        # EKS/ACK/TKE 节点变更
        if (("eks" in content_lower and "node" in content_lower) or 
            ("ack" in content_lower and "node" in content_lower) or
            ("tke" in content_lower and "node" in content_lower)):
            if platform_lower == "aws":
                return "AWS_EKS_NODE_GROUP_SCALING_TF"
        
        # 实例类型变更
        if "instance" in content_lower and ("type" in content_lower or "class" in content_lower):
            if "rds" in content_lower and platform_lower == "aws":
                return "AWS_RDS_INSTANCE_CLASS_CHANGE_TF"
        
        # 镜像ID变更
        if "image" in content_lower and ("id" in content_lower or "ami" in content_lower):
            if platform_lower == "tencentcloud":
                return "TENCENTCLOUD_CVM_IMAGE_UPDATE_TF"
    
    return ""

def _extract_kubernetes_changes(yaml_content: str) -> str:
    """提取 Kubernetes YAML 变更的关键信息"""
    # 尝试提取变更前后内容
    before_after_parts = re.split(r'---\s*#\s*变更[前后]|---\s*变更[前后]', yaml_content)
    
    if len(before_after_parts) >= 3:
        # 有明确的变更前后标记
        summary = []
        
        # 提取资源类型和名称
        kind_match = re.search(r"kind:\s*['\"]?([^'\"\n]+)['\"]?", yaml_content)
        name_match = re.search(r"name:\s*['\"]?([^'\"\n]+)['\"]?", yaml_content)
        
        if kind_match:
            summary.append(f"资源类型: {kind_match.group(1)}")
        if name_match:
            summary.append(f"资源名称: {name_match.group(1)}")
        
        # 提取变更描述
        change_desc = ""
        if "变更将" in yaml_content or "本次变更" in yaml_content:
            desc_match = re.search(r'[本次]*变更将.*', yaml_content)
            if desc_match:
                change_desc = desc_match.group(0)
        
        if change_desc:
            summary.append(f"变更描述: {change_desc}")
        else:
            # 自动检测差异
            before = before_after_parts[1]
            after = before_after_parts[2]
            diff = difflib.ndiff(before.splitlines(), after.splitlines())
            changes = "\n".join([line for line in diff if line.startswith('+ ') or line.startswith('- ')])
            summary.append(f"变更差异: {changes[:500]}")  # 限制差异长度
        
        return "\n".join(summary)
    
    # 没有明确的变更前后标记，直接返回处理后的内容
    result = []
    
    # 提取资源类型和名称
    kind_match = re.search(r"kind:\s*['\"]?([^'\"\n]+)['\"]?", yaml_content)
    name_match = re.search(r"name:\s*['\"]?([^'\"\n]+)['\"]?", yaml_content)
    
    if kind_match:
        result.append(f"资源类型: {kind_match.group(1)}")
    if name_match:
        result.append(f"资源名称: {name_match.group(1)}")
    
    # 提取关键配置字段
    if "ingress" in yaml_content.lower():
        paths = re.findall(r"path:\s*([^\n]+)", yaml_content)
        if paths:
            result.append(f"路径配置: {', '.join(paths)}")
        
        hosts = re.findall(r"host:\s*([^\n]+)", yaml_content)
        if hosts:
            result.append(f"主机配置: {', '.join(hosts)}")
    
    if "deployment" in yaml_content.lower():
        replicas = re.search(r"replicas:\s*(\d+)", yaml_content)
        if replicas:
            result.append(f"副本数: {replicas.group(1)}")
        
        image = re.search(r"image:\s*([^\n]+)", yaml_content)
        if image:
            result.append(f"镜像: {image.group(1)}")
    
    if not result:
        # 如果没提取到关键信息，返回前300个字符作为摘要
        return yaml_content[:300]
    
    return "\n".join(result)

def _extract_terraform_changes(tf_content: str) -> str:
    """提取 Terraform 变更的关键信息"""
    result = []
    
    # 尝试识别资源类型
    resource_matches = re.findall(r"resource\s+['\"]([^'\"]+)['\"]", tf_content)
    if resource_matches:
        result.append(f"Terraform资源类型: {', '.join(resource_matches)}")
    
    # 尝试提取变量赋值
    var_matches = re.findall(r"(\w+)\s*=\s*['\"]?([^'\"\n]+)['\"]?", tf_content)
    if var_matches:
        vars_str = ", ".join([f"{k}={v}" for k, v in var_matches[:5]])  # 限制数量
        result.append(f"关键配置: {vars_str}")
    
    # 尝试提取变更描述
    if "变更将" in tf_content or "本次变更" in tf_content:
        desc_match = re.search(r'[本次]*变更将.*', tf_content)
        if desc_match:
            result.append(f"变更描述: {desc_match.group(0)}")
    
    if not result:
        # 如果没提取到关键信息，返回前300个字符作为摘要
        return tf_content[:300]
    
    return "\n".join(result)

def match_change_with_knowledge_base(change_type: str, content: str, kb: Dict) -> Optional[Dict[str, Any]]:
    """
    将预处理后的变更与知识库进行匹配
    
    Args:
        change_type: 变更类型
        content: 预处理后的变更内容
        kb: 知识库内容
        
    Returns:
        Dict: 匹配到的知识库项，或None表示未找到匹配
    """
    # 无法识别变更类型时，返回None
    if not change_type:
        return None
    
    content_lower = content.lower()
    change_items = kb.get("change_items", [])
    best_match = None
    best_score = 0
    
    # 精确匹配：类型完全一致
    for item in change_items:
        if item.get("type") == change_type:
            return item
    
    # 部分匹配：类型部分一致
    change_type_parts = change_type.split("_")
    for item in change_items:
        item_type = item.get("type", "")
        item_type_parts = item_type.split("_")
        
        # 计算匹配分数
        match_score = 0
        
        # 1. 类型部分匹配
        for part in change_type_parts:
            if part in item_type:
                match_score += 1
        
        # 2. 描述关键词匹配
        description = item.get("description", "").lower()
        for part in change_type_parts:
            if part.lower() in description:
                match_score += 0.5
        
        # 3. 云厂商匹配
        cloud_providers = item.get("cloud_providers", [])
        for part in change_type_parts:
            if part in cloud_providers:
                match_score += 2
        
        # 4. 内容关键字匹配
        description = item.get("description", "").lower()
        description_words = set(description.split())
        content_words = set(content_lower.split())
        common_words = description_words.intersection(content_words)
        match_score += len(common_words) * 0.1
        
        if match_score > best_score:
            best_score = match_score
            best_match = item
    
    # 设定匹配阈值
    if best_score >= 1:
        return best_match
    
    return None 