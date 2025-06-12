import os
import requests
import json
import time
import traceback

# API 端点
API_URL = "http://localhost:8001"

def test_case_1():
    """低风险测试用例"""
    code = """def add_numbers(a: int, b: int) -> int:
    return a + b"""
    return requests.post(f"{API_URL}/predict", json={"code": code})

def test_case_2():
    """中风险测试用例"""
    code = """def execute_command(cmd: str) -> str:
    import subprocess
    return subprocess.check_output(cmd, shell=True)"""
    return requests.post(f"{API_URL}/predict", json={"code": code})

def test_case_3():
    """高风险测试用例"""
    code = """def execute_command(cmd):
    import os
    os.system(cmd)  # 直接执行系统命令，存在命令注入风险"""
    return requests.post(f"{API_URL}/predict", json={"code": code})

def run_tests():
    """运行所有测试用例"""
    print("开始运行测试用例...")
    
    try:
        # 测试用例 1
        print("\n运行测试用例 1 (低风险)...")
        response = test_case_1()
        if response.status_code == 200:
            print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        else:
            print(f"错误: HTTP {response.status_code} - {response.text}")
        time.sleep(2)  # 等待数据写入 InfluxDB
        
        # 测试用例 2
        print("\n运行测试用例 2 (中风险)...")
        response = test_case_2()
        if response.status_code == 200:
            print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        else:
            print(f"错误: HTTP {response.status_code} - {response.text}")
        time.sleep(2)
        
        # 测试用例 3
        print("\n运行测试用例 3 (高风险)...")
        response = test_case_3()
        if response.status_code == 200:
            print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        else:
            print(f"错误: HTTP {response.status_code} - {response.text}")
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    run_tests() 