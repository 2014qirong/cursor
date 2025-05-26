from typing import Dict

class OPAEngine:
    """
    OPA规则引擎集成，实际项目中可通过HTTP API与OPA服务交互。
    这里为伪实现。
    """
    def __init__(self):
        # 可加载本地策略或配置OPA服务地址
        pass

    def decide(self, risk_level: str, nlp_result: str) -> Dict:
        """
        根据AI分析结果和策略规则做出决策
        :param risk_level: AI风险等级
        :param nlp_result: NLP分析结果
        :return: 决策结果（允许/阻断/警告）
        """
        # 伪实现
        if risk_level == "高" or "高风险" in nlp_result:
            return {"decision": "阻断", "reason": "高风险变更"}
        elif risk_level == "中":
            return {"decision": "警告", "reason": "需人工审核"}
        else:
            return {"decision": "允许", "reason": "低风险"}

# 单例
opa_engine = OPAEngine() 