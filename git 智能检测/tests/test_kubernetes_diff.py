import requests
import json

# 高风险变更示例
high_risk_diff = """
直接暴露密码: supersecret123
暴露敏感配置: DB_PASSWORD=supersecret123
直接暴露密钥: secretKeyRef: supersecret123
"""

# 低风险变更示例
low_risk_diff = """
添加资源限制: cpu: 250m, memory: 500m
添加资源限制: cpu: 500m, memory: 1Gi
添加资源限制: cpu: 100m, memory: 200m
"""

# 调用AI推理服务
def call_ai_service(diff_content):
    response = requests.post("http://localhost:8001/predict", json={"diff": diff_content})
    return response.json()

# 调用LIME解释服务
def call_lime_service(diff_content):
    response = requests.post("http://localhost:8002/explain", json={"diff": diff_content})
    return response.json()

# 验证高风险变更
print("=== 高风险变更测试 ===")
high_risk_result = call_ai_service(high_risk_diff)
print("AI推理服务结果:")
print(high_risk_result)
high_risk_explanation = call_lime_service(high_risk_diff)
print("LIME解释服务结果:")
print(high_risk_explanation)

# 验证低风险变更
print("=== 低风险变更测试 ===")
low_risk_result = call_ai_service(low_risk_diff)
print("AI推理服务结果:")
print(low_risk_result)
low_risk_explanation = call_lime_service(low_risk_diff)
print("LIME解释服务结果:")
print(low_risk_explanation)

if __name__ == "__main__":
    test_high_risk_diff()
    test_low_risk_diff() 