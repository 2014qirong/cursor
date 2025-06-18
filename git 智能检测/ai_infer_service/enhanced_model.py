import json
from typing import Dict, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EnhancedRiskModel:
    def __init__(self, base_model, knowledge_base_path: str):
        self.base_model = base_model
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.vectorizer = TfidfVectorizer()
        self._prepare_vectors()
    
    def _load_knowledge_base(self, path: str) -> Dict:
        """加载知识库"""
        with open(path, 'r') as f:
            return json.load(f)
    
    def _prepare_vectors(self):
        """准备文档向量"""
        try:
            # 检查知识库格式并适配不同的结构
            if 'risk_patterns' in self.knowledge_base:
                # 原始格式
                risk_docs = [pattern['content'] for pattern in self.knowledge_base.get('risk_patterns', [])]
            elif 'change_items' in self.knowledge_base:
                # 新格式 - 使用 change_items 中的 description 字段
                risk_docs = [item['description'] for item in self.knowledge_base.get('change_items', [])]
            else:
                risk_docs = []
                print("警告: 知识库中没有找到可用的风险模式数据")
                
            if risk_docs:  # 只有在有文档时才进行向量化
                self.risk_vectors = self.vectorizer.fit_transform(risk_docs)
            else:
                self.risk_vectors = None
                print("警告: 风险模式文档为空")
            
            # 准备解决方案文档 - 同样适配不同格式
            if 'solutions' in self.knowledge_base:
                # 原始格式
                solution_docs = [sol['content'] for sol in self.knowledge_base.get('solutions', [])]
            elif 'change_items' in self.knowledge_base:
                # 新格式 - 使用 change_items 中的 mitigation_strategies 字段
                solution_docs = []
                for item in self.knowledge_base.get('change_items', []):
                    if 'mitigation_strategies' in item:
                        solution_docs.extend(item['mitigation_strategies'])
            else:
                solution_docs = []
                
            if solution_docs and self.risk_vectors is not None:  # 使用已训练的向量器
                self.solution_vectors = self.vectorizer.transform(solution_docs)
            else:
                self.solution_vectors = None
                print("警告: 解决方案文档为空或风险向量未初始化")
        except Exception as e:
            print(f"向量准备错误: {str(e)}")
            self.risk_vectors = None
            self.solution_vectors = None
    
    def predict(self, code: str) -> Dict:
        """预测风险"""
        # 基础模型预测
        try:
            # 使用包装后的基础模型进行预测
            if isinstance(self.base_model, type) and hasattr(self.base_model, 'predict_proba'):
                base_prob = float(self.base_model.predict_proba([code])[0][1])  # 获取正类的概率
            else:
                # 如果是字典、简单模型或其他类型，假设默认为中等风险
                print("基础模型不支持 predict_proba 方法，使用默认风险值")
                base_prob = 0.5
        except Exception as e:
            print(f"基础模型预测错误: {str(e)}")
            base_prob = 0.5  # 如果基础模型预测失败，使用默认值
        
        # 知识库匹配
        matched_pattern = None
        suggested_solution = None
        max_risk_sim = 0.0
        
        if self.risk_vectors is not None:
            try:
                # 确保 code 是字符串类型
                if not isinstance(code, str):
                    code = str(code)
                
                # 确保 vectorizer 已经拟合过
                if hasattr(self.vectorizer, 'vocabulary_'):
                    code_vector = self.vectorizer.transform([code])
                else:
                    # 如果 vectorizer 没有拟合过，先用当前输入拟合
                    code_vector = self.vectorizer.fit_transform([code])
                
                # 计算与风险模式的相似度
                risk_similarities = cosine_similarity(code_vector, self.risk_vectors)[0]
                if len(risk_similarities) > 0:
                    max_risk_sim = max(risk_similarities)
                    risk_index = np.argmax(risk_similarities)
                    
                    # 根据知识库格式获取匹配的模式
                    if 'risk_patterns' in self.knowledge_base:
                        matched_pattern = self.knowledge_base['risk_patterns'][risk_index]
                    elif 'change_items' in self.knowledge_base:
                        item = self.knowledge_base['change_items'][risk_index]
                        matched_pattern = {
                            'id': item.get('type', f'PATTERN_{risk_index}'),
                            'content': item.get('description', ''),
                            'risk_level': item.get('risk_level', 'Medium'),
                            'tags': item.get('cloud_providers', []) + item.get('management_tools', []),
                            'key_metrics_to_monitor': item.get('key_metrics_to_monitor', []),
                            'potential_impacts': item.get('potential_impacts', []),
                            'mitigation_strategies': item.get('mitigation_strategies', [])
                        }
                
                # 获取相关的解决方案
                if self.solution_vectors is not None and len(self.solution_vectors.toarray()) > 0:
                    solution_similarities = cosine_similarity(code_vector, self.solution_vectors)[0]
                    if len(solution_similarities) > 0:
                        solution_index = np.argmax(solution_similarities)
                        
                        # 根据知识库格式获取匹配的解决方案
                        if 'solutions' in self.knowledge_base:
                            suggested_solution = self.knowledge_base['solutions'][solution_index]
                        elif 'change_items' in self.knowledge_base and matched_pattern:
                            # 从匹配的模式中获取解决方案
                            pattern_id = matched_pattern.get('id')
                            for item in self.knowledge_base.get('change_items', []):
                                if item.get('type') == pattern_id and 'mitigation_strategies' in item:
                                    strategy = item['mitigation_strategies'][0]  # 获取第一个缓解策略
                                    suggested_solution = {
                                        'id': f"{pattern_id}_SOL_0",
                                        'pattern_id': pattern_id,
                                        'content': strategy,
                                        'source': 'knowledge_base'
                                    }
                                    break
            except Exception as e:
                print(f"知识库匹配错误: {str(e)}")
        
        # 综合评估
        if matched_pattern:
            enhanced_prob = self._combine_probabilities(base_prob, max_risk_sim)
        else:
            enhanced_prob = base_prob
        
        result = {
            'probability': float(enhanced_prob),  # 确保概率值是 float 类型
            'risk_level': self._get_risk_level(enhanced_prob),
        }
        
        if matched_pattern:
            result['matched_pattern'] = matched_pattern
            # 补充结构化风险信息
            for field in [
                'key_metrics_to_monitor',
                'potential_impacts',
                'mitigation_strategies'
            ]:
                if field in matched_pattern:
                    result['matched_pattern'].setdefault(field, matched_pattern[field])
        if suggested_solution:
            result['suggested_solution'] = suggested_solution
            
        return result
    
    def _combine_probabilities(self, base_prob: float, pattern_sim: float) -> float:
        """综合概率计算"""
        # 使用加权平均
        w1, w2 = 0.7, 0.3  # 权重可调
        return w1 * base_prob + w2 * pattern_sim
    
    def _get_risk_level(self, prob: float) -> str:
        """获取风险等级"""
        if prob >= 0.7:
            return "高风险"
        elif prob >= 0.5:
            return "中风险"
        else:
            return "低风险"
    
    def explain(self, code: str) -> Dict:
        """解释预测结果"""
        prediction = self.predict(code)
        
        # 构建解释
        explanation = {
            'risk_probability': prediction['probability'],
            'risk_level': prediction['risk_level'],
        }
        
        if 'matched_pattern' in prediction:
            explanation['matched_pattern'] = {
                'description': prediction['matched_pattern'].get('content', ''),
                'source': prediction['matched_pattern'].get('source', 'knowledge_base')
            }
        
        if 'suggested_solution' in prediction:
            explanation['solution'] = {
                'description': prediction['suggested_solution'].get('content', ''),
                'source': prediction['suggested_solution'].get('source', 'knowledge_base')
            }
        
        explanation['relevant_abbreviations'] = self._find_relevant_abbreviations(code)
        
        return explanation
    
    def _find_relevant_abbreviations(self, code: str) -> Dict[str, str]:
        """查找相关缩略语"""
        relevant = {}
        try:
            # 尝试从知识库中获取缩略语
            if 'abbreviations' in self.knowledge_base:
                # 原始格式
                abbreviations = self.knowledge_base.get('abbreviations', {})
                for abbr, full in abbreviations.items():
                    if abbr in code:
                        relevant[abbr] = full
            elif 'change_items' in self.knowledge_base:
                # 新格式 - 从 change_items 中提取缩略语
                # 这里我们将云服务提供商和管理工具的缩写作为缩略语
                cloud_abbrs = {}
                tool_abbrs = {}
                
                # 收集所有云服务提供商和管理工具
                for item in self.knowledge_base.get('change_items', []):
                    # 云服务提供商缩写
                    for provider in item.get('cloud_providers', []):
                        if provider in ['AWS', 'AliCloud', 'TencentCloud', 'GCP', 'Azure']:
                            if provider == 'AWS':
                                cloud_abbrs[provider] = 'Amazon Web Services'
                            elif provider == 'AliCloud':
                                cloud_abbrs[provider] = 'Alibaba Cloud'
                            elif provider == 'TencentCloud':
                                cloud_abbrs[provider] = 'Tencent Cloud'
                            elif provider == 'GCP':
                                cloud_abbrs[provider] = 'Google Cloud Platform'
                            elif provider == 'Azure':
                                cloud_abbrs[provider] = 'Microsoft Azure'
                    
                    # 管理工具缩写
                    for tool in item.get('management_tools', []):
                        if tool in ['K8s', 'TF', 'CF', 'CDK', 'Helm', 'ArgoCD']:
                            if tool == 'K8s':
                                tool_abbrs[tool] = 'Kubernetes'
                            elif tool == 'TF':
                                tool_abbrs[tool] = 'Terraform'
                            elif tool == 'CF':
                                tool_abbrs[tool] = 'CloudFormation'
                            elif tool == 'CDK':
                                tool_abbrs[tool] = 'Cloud Development Kit'
                            elif tool == 'ArgoCD':
                                tool_abbrs[tool] = 'Argo CD'
                
                # 检查代码中是否包含这些缩略语
                for abbr, full in {**cloud_abbrs, **tool_abbrs}.items():
                    if abbr in code:
                        relevant[abbr] = full
        except Exception as e:
            print(f"查找缩略语错误: {str(e)}")
        return relevant
    
    def _match_patterns(self, text: str, top_n: int = 3) -> List[Dict]:        
        """匹配风险模式"""
        if not text or self.risk_vectors is None:
            return []
        
        # 向量化输入文本
        text_vector = self.vectorizer.transform([text])
        
        # 计算相似度
        similarities = cosine_similarity(text_vector, self.risk_vectors).flatten()
        
        # 获取前N个最相似的模式
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # 设置一个最小相似度阈值
                if 'risk_patterns' in self.knowledge_base:
                    # 原始格式
                    pattern = self.knowledge_base['risk_patterns'][idx]
                    results.append({
                        'pattern': pattern,
                        'similarity': float(similarities[idx])
                    })
                elif 'change_items' in self.knowledge_base:
                    # 新格式
                    item = self.knowledge_base['change_items'][idx]
                    results.append({
                        'pattern': {
                            'id': item.get('type', f'PATTERN_{idx}'),
                            'content': item.get('description', ''),
                            'risk_level': item.get('risk_level', 'Medium'),
                            'tags': item.get('cloud_providers', []) + item.get('management_tools', [])
                        },
                        'similarity': float(similarities[idx])
                    })
        
        return results
    
    def _get_solutions(self, pattern_id: str) -> List[Dict]:
        """获取解决方案"""
        if 'solutions' in self.knowledge_base:
            # 原始格式
            return [sol for sol in self.knowledge_base.get('solutions', []) 
                    if sol.get('pattern_id') == pattern_id]
        elif 'change_items' in self.knowledge_base:
            # 新格式
            for item in self.knowledge_base.get('change_items', []):
                if item.get('type') == pattern_id:
                    return [{
                        'id': f"{pattern_id}_SOL_{i}",
                        'pattern_id': pattern_id,
                        'content': strategy,
                        'tags': item.get('cloud_providers', []) + item.get('management_tools', [])
                    } for i, strategy in enumerate(item.get('mitigation_strategies', []))]
        return []