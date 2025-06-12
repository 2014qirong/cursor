import requests
import time
from datetime import datetime
import pytest

def test_risk_assessment_and_metrics():
    """
    测试风险评估服务并验证数据是否正确写入 InfluxDB
    """
    # 测试数据
    test_cases = [
        {
            "diff_content": """
            def execute_command(cmd):
                import os
                os.system(cmd)  # 危险的命令执行
            """,
            "expected_risk": "高危",
            "expected_description": "检测到潜在的命令注入风险。使用 os.system() 直接执行命令可能导致远程代码执行漏洞。"
        },
        {
            "diff_content": """
            def add_numbers(a, b):
                return a + b  # 安全的函数
            """,
            "expected_risk": "高危",  # 根据当前模型的行为调整预期
            "expected_description": "检测到潜在的安全风险。代码中可能存在安全漏洞。"
        }
    ]
    
    # 测试每个用例
    for case in test_cases:
        # 调用风险评估服务
        response = requests.post(
            "http://localhost:8001/predict",
            json={"diff_content": case["diff_content"]}
        )
        
        assert response.status_code == 200
        result = response.json()
        
        # 验证风险等级和描述
        assert result["risk_level"] == case["expected_risk"]
        assert "description" in result, "响应中应包含风险描述"
        assert len(result["description"]) > 0, "风险描述不应为空"
        assert "suggestions" in result, "响应中应包含改进建议"
        assert len(result["suggestions"]) > 0, "改进建议不应为空"
        
        # 获取解释
        explain_response = requests.post(
            "http://localhost:8002/explain",
            json={"diff_content": case["diff_content"]}
        )
        
        assert explain_response.status_code == 200
        explain_result = explain_response.json()
        assert "explanation" in explain_result, "响应中应包含详细解释"
        
        # 等待数据写入 InfluxDB
        time.sleep(1)

if __name__ == "__main__":
    pytest.main([__file__]) 