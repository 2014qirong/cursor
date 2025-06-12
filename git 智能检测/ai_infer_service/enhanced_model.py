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
            # 准备风险模式文档
            risk_docs = [pattern['content'] for pattern in self.knowledge_base.get('risk_patterns', [])]
            if risk_docs:  # 只有在有文档时才进行向量化
                self.risk_vectors = self.vectorizer.fit_transform(risk_docs)
            else:
                self.risk_vectors = None
                print("警告: 风险模式文档为空")
            
            # 准备解决方案文档
            solution_docs = [sol['content'] for sol in self.knowledge_base.get('solutions', [])]
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
                    matched_pattern = self.knowledge_base['risk_patterns'][risk_index]
                
                # 获取相关的解决方案
                if self.solution_vectors is not None and len(self.solution_vectors.toarray()) > 0:
                    solution_similarities = cosine_similarity(code_vector, self.solution_vectors)[0]
                    if len(solution_similarities) > 0:
                        solution_index = np.argmax(solution_similarities)
                        suggested_solution = self.knowledge_base['solutions'][solution_index]
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
                'description': prediction['matched_pattern']['content'],
                'source': prediction['matched_pattern']['source']
            }
        
        if 'suggested_solution' in prediction:
            explanation['solution'] = {
                'description': prediction['suggested_solution']['content'],
                'source': prediction['suggested_solution']['source']
            }
        
        explanation['relevant_abbreviations'] = self._find_relevant_abbreviations(code)
        
        return explanation
    
    def _find_relevant_abbreviations(self, code: str) -> Dict[str, str]:
        """查找相关缩略语"""
        relevant = {}
        try:
            abbreviations = self.knowledge_base.get('abbreviations', {})
            for abbr, full in abbreviations.items():
                if abbr in code:
                    relevant[abbr] = full
        except Exception as e:
            print(f"查找缩略语错误: {str(e)}")
        return relevant 