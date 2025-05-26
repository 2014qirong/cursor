import requests
import os
from typing import Dict

AI_INFER_URL = os.getenv("AI_INFER_URL", "http://localhost:8001/predict")

class AIRiskAnalyzer:
    """
    AI风险分析服务，集成分类模型（Scikit-learn）和NLP模型（BERT）。
    实际项目中应加载训练好的模型，这里为伪实现。
    """
    def __init__(self):
        pass  # 不再本地加载模型

    def classify_risk(self, diff: str) -> str:
        """
        使用Scikit-learn模型对diff内容进行风险分类
        :param diff: 代码变更diff文本
        :return: 风险等级（高/中/低）
        """
        resp = requests.post(AI_INFER_URL, json={"diff": diff}, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("risk_level", "未知")
        return "未知"

    def nlp_risk(self, diff: str) -> str:
        """
        使用BERT等NLP模型对diff内容进行语义风险分析
        :param diff: 代码变更diff文本
        :return: NLP分析结果
        """
        # 伪实现
        if "kubernetes" in diff or "ingress" in diff:
            return "涉及K8s高风险"
        return "无明显风险"

    def analyze(self, diff: str) -> Dict:
        """
        综合分析接口，返回风险等级和NLP分析结果
        """
        resp = requests.post(AI_INFER_URL, json={"diff": diff}, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "risk_level": data.get("risk_level", "未知"),
                "prob": data.get("prob", [])
            }
        return {"risk_level": "未知", "prob": []}

# 单例
ai_analyzer = AIRiskAnalyzer() 