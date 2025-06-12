import json
import os
import re
import yaml
from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util
import numpy as np

# 模型配置
EMBEDDING_MODEL = 'paraphrase-multilingual-MiniLM-L12-v2'  # 支持中英文的轻量级多语言模型
SIMILARITY_THRESHOLD = 0.4  # 语义相似度阈值，降低阈值以匹配更多场景

# 初始化语义模型（延迟加载，只在需要时初始化）
_model = None
_kb_embeddings = None
_kb_descriptions = None

def get_model():
    global _model, _kb_embeddings, _kb_descriptions
    if _model is None:
        try:
            print(f"初始化语义模型: {EMBEDDING_MODEL}...")
            _model = SentenceTransformer(EMBEDDING_MODEL)
            # 预计算知识库的嵌入向量
            _kb_descriptions = [item.get('description', '') for item in kb]
            _kb_embeddings = _model.encode(_kb_descriptions, convert_to_tensor=True)
            print(f"语义模型初始化完成，知识库条目数: {len(kb)}")
        except Exception as e:
            print(f"语义模型初始化失败: {e}")
            print("将使用简单文本相似度作为后备方案")
    return _model

# 加载知识库
def load_knowledge_base(kb_file='cloud_change_risk_assessment_kb.json'):
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb = json.load(f)
            print(f"知识库加载成功，包含 {len(kb['risk_patterns'])} 个风险模式。")
            
        # 加载CDN风险模式
        try:
            with open('cdn_risk_patterns.json', 'r', encoding='utf-8') as f:
                cdn_kb = json.load(f)
                print(f"CDN风险模式加载成功，包含 {len(cdn_kb['risk_patterns'])} 个风险模式。")
                # 合并风险模式
                kb['risk_patterns'].extend(cdn_kb['risk_patterns'])
                print(f"合并后知识库包含 {len(kb['risk_patterns'])} 个风险模式。")
        except Exception as e:
            print(f"加载CDN风险模式失败: {e}")
            
        return kb
    except Exception as e:
        print(f"加载知识库失败: {e}")
        return {'risk_patterns': []}

# 资源类型关键词映射（可扩展）
resource_type_keywords = {
    'k8s': ['kubernetes', 'k8s', 'pod', 'deployment', 'service', 'ingress', 'namespace', 'configmap', 'secret'],
    'database': ['database', 'db', 'sql', 'nosql', 'redis', 'mongodb', 'mysql', 'postgresql', 'oracle', 'dynamodb'],
    'security_group': ['security group', 'firewall', 'network acl', 'nacl', 'security policy'],
    'cdn': ['cdn', 'content delivery network', 'cloudfront', 'akamai', 'fastly', 'waf', 'web application firewall'],
    'load_balancer': ['load balancer', 'elb', 'alb', 'nlb', 'slb', 'clb'],
    'waf': ['waf', 'web application firewall', 'firewall', 'security protection']
}

# 加载知识库
kb = load_knowledge_base()
risk_patterns = kb.get('risk_patterns', [])

RESOURCE_KEYWORDS = {
    'dns': ['dns', 'route53', '云解析', 'cname', 'a记录', 'mx记录'],
    'k8s': ['k8s', 'kubernetes', 'ingress', 'deployment', 'statefulset', 'pod'],
    'loadbalancer': ['elb', 'clb', 'slb', 'loadbalancer', 'listener', 'forward'],
    'database': ['rds', 'mysql', 'postgres', 'dbinstance', '数据库'],
    'objectstorage': ['oss', 's3', 'cos', 'bucket', 'object storage', 'bucket policy', 'policy', '存储桶', '授权策略', 'getobject', 'putobject'],
    'cdn': ['cdn', 'cloudfront'],
    'waf': ['waf'],
    'securitygroup': ['sg', 'security group', '安全组'],
    'vpc': ['vpc', 'route table', '路由表', 'vpc router', 'gateway', 'igw', 'vgw', '路由', 'routetableid'],
    'ga': ['global accelerator', 'ga', '全球加速'],
    'cen': ['cen', 'ccn', 'transit gateway', '云企业网', '云联网'],
    'cache': ['redis', 'cache', 'memcached'],
    'mq': ['kafka', 'rabbitmq', '消息队列', 'topic', 'vhost'],
}

# 简单的资源类型识别
def detect_resource_type(text: str) -> List[str]:
    found = []
    for k, keywords in RESOURCE_KEYWORDS.items():
        for kw in keywords:
            if re.search(rf'\b{re.escape(kw)}\b', text, re.IGNORECASE):
                found.append(k)
                break
    return found

# 解析YAML/Terraform/JSON/文本
def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if ext in ['.yaml', '.yml']:
        try:
            data = yaml.safe_load(content)
            return json.dumps(data, ensure_ascii=False)
        except Exception:
            return content
    elif ext in ['.json']:
        return content
    else:
        return content

# 简单文本相似度（作为后备方案）
def simple_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# 使用语义模型计算相似度
def semantic_similarity(query: str, candidates: List[str]) -> List[float]:
    model = get_model()
    if model is None:
        # 模型加载失败，使用简单相似度作为后备方案
        return [simple_similarity(query, cand) for cand in candidates]
    
    # 计算查询文本的嵌入向量
    query_embedding = model.encode(query, convert_to_tensor=True)
    # 计算与知识库的相似度
    similarities = util.cos_sim(query_embedding, _kb_embeddings)[0].cpu().numpy()
    return similarities

# 优化的场景匹配
def match_scenario(input_text: str, resource_types: List[str], topk=3, threshold=SIMILARITY_THRESHOLD) -> List[Tuple[float, Dict[str, Any]]]:
    # 资源类型预筛选
    candidates_idx = []
    for i, item in enumerate(kb):
        # 资源类型粗筛
        type_text = (item.get('type', '') + ' ' + item.get('description', '')).lower()
        if not resource_types or any(rt in type_text for rt in resource_types):
            candidates_idx.append(i)
    
    # 如果没有资源类型匹配，则考虑所有条目
    if not candidates_idx:
        candidates_idx = list(range(len(kb)))
    
    try:
        # 语义相似度计算
        model = get_model()
        if model is not None:
            # 使用预计算的嵌入向量
            query_embedding = model.encode(input_text, convert_to_tensor=True)
            # 只计算候选项的相似度
            if len(candidates_idx) == len(kb):
                similarities = util.cos_sim(query_embedding, _kb_embeddings)[0].cpu().numpy()
            else:
                candidate_embeddings = _kb_embeddings[candidates_idx]
                similarities = util.cos_sim(query_embedding, candidate_embeddings)[0].cpu().numpy()
                # 调整相似度索引映射回原始索引
                full_similarities = np.zeros(len(kb))
                for i, idx in enumerate(candidates_idx):
                    full_similarities[idx] = similarities[i]
                similarities = full_similarities
            
            # 按相似度排序
            results = [(similarities[i], kb[i]) for i in range(len(kb)) 
                      if i in candidates_idx and similarities[i] >= threshold]
            results.sort(reverse=True, key=lambda x: x[0])
            return results[:topk]
    except Exception as e:
        print(f"语义匹配出错: {e}，使用简单相似度作为后备方案")
    
    # 后备方案：简单文本相似度
    candidates = []
    for i in candidates_idx:
        sim = simple_similarity(input_text, kb[i].get('description', ''))
        candidates.append((sim, kb[i]))
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[:topk]

# 风险输出
def predict_risk(change_text, resource_types=None):
    """预测变更风险"""
    # 如果没有指定资源类型，则尝试从文本中识别
    if not resource_types:
        resource_types = identify_resource_types(change_text)
        print(f"识别到的资源类型: {', '.join(resource_types)}")
    
    # 过滤知识库中与资源类型相关的风险模式
    filtered_patterns = []
    for pattern in risk_patterns:
        # 检查模式是否与任一资源类型相关
        pattern_text = json.dumps(pattern, ensure_ascii=False).lower()
        if any(rt in pattern_text for rt in resource_types):
            filtered_patterns.append(pattern)
    
    if not filtered_patterns:
        print("未找到与资源类型匹配的风险模式，将使用全部风险模式")
        filtered_patterns = risk_patterns
    
    # 计算语义相似度并找出最匹配的风险模式
    best_matches = find_best_matches(change_text, filtered_patterns)
    
    if not best_matches:
        return {
            "risk_level": "未知",
            "matched_patterns": [],
            "description": "未能识别相关风险场景，建议人工评估",
            "suggestions": ["请安排专业人员进行人工评估"]
        }
    
    # 提取最高风险等级
    risk_levels = {
        "Critical": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1,
        "未知": 0
    }
    
    highest_risk = max(best_matches, key=lambda x: risk_levels.get(x["pattern"].get("risk_level", "未知"), 0))
    highest_risk_level = highest_risk["pattern"].get("risk_level", "未知")
    
    # 风险等级中英文映射
    risk_level_map = {
        "Critical": "严重风险",
        "High": "高风险",
        "Medium": "中风险",
        "Low": "低风险",
        "未知": "未知"
    }
    
    # 构建风险描述和建议
    description = highest_risk["pattern"].get("description", "")
    suggestions = []
    
    # 添加预检查项
    pre_checklist = highest_risk["pattern"].get("pre_change_checklist", [])
    if pre_checklist:
        suggestions.extend([f"变更前检查: {item}" for item in pre_checklist])
    
    # 添加变更后验证项
    post_verification = highest_risk["pattern"].get("post_change_verification", [])
    if post_verification:
        suggestions.extend([f"变更后验证: {item}" for item in post_verification])
    
    # 添加缓解策略
    mitigation = highest_risk["pattern"].get("mitigation_strategies", [])
    if mitigation:
        suggestions.extend([f"缓解策略: {item}" for item in mitigation])
    
    # 返回结果
    return {
        "risk_level": risk_level_map.get(highest_risk_level, "未知"),
        "matched_patterns": [{
            "type": m["pattern"].get("type", "未知"),
            "similarity": m["similarity"],
            "risk_level": risk_level_map.get(m["pattern"].get("risk_level", "未知"), "未知")
        } for m in best_matches],
        "description": description,
        "suggestions": suggestions
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="云变更风险智能预判工具")
    parser.add_argument('file', help='待分析的变更文件（支持YAML/Terraform/JSON/文本）')
    parser.add_argument('--threshold', type=float, default=SIMILARITY_THRESHOLD, 
                        help=f'语义相似度阈值，默认为{SIMILARITY_THRESHOLD}')
    parser.add_argument('--simple', action='store_true', help='使用简单文本相似度（不使用语义模型）')
    parser.add_argument('--topk', type=int, default=3, help='返回最相似的前K个结果，默认为3')
    
    args = parser.parse_args()
    
    # 应用命令行参数
    if args.simple:
        # 强制使用简单相似度
        _model = None
        print("已禁用语义模型，将使用简单文本相似度")
    
    # 通过参数传递而不是全局变量修改
    predict_risk(args.file, threshold=args.threshold, topk=args.topk)


def identify_resource_types(text):
    """从文本中识别资源类型"""
    identified_types = []
    text_lower = text.lower()
    
    for resource_type, keywords in resource_type_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            identified_types.append(resource_type)
    
    return identified_types

def find_best_matches(change_text, patterns, topk=3, threshold=SIMILARITY_THRESHOLD):
    """找出最匹配的风险模式"""
    matches = []
    
    for pattern in patterns:
        # 将模式转换为文本进行相似度计算
        pattern_text = json.dumps(pattern, ensure_ascii=False)
        
        # 计算简单文本相似度（作为备选）
        simple_similarity = simple_text_similarity(change_text, pattern_text)
        
        # 计算语义相似度（如果模型已初始化）
        semantic_similarity = semantic_similarity_score(change_text, pattern_text)
        
        # 使用语义相似度，如果无法计算则使用简单文本相似度
        similarity = semantic_similarity if semantic_similarity is not None else simple_similarity
        
        if similarity >= threshold:
            matches.append({
                "pattern": pattern,
                "similarity": similarity
            })
    
    # 按相似度排序并返回前topk个
    matches.sort(key=lambda x: x["similarity"], reverse=True)
    return matches[:topk]