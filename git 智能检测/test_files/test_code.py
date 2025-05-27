def hello_world():
    """
    一个简单的测试函数
    """
    print("Hello, World!")
    return "Hello, World!"

def add_numbers(a: int, b: int) -> int:
    """
    简单的加法函数
    """
    return a + b

def execute_command(cmd: str) -> str:
    """
    执行系统命令的函数 - 这应该会触发风险评估
    """
    import os
    import subprocess
    result = subprocess.check_output(cmd, shell=True)
    return result.decode('utf-8') 