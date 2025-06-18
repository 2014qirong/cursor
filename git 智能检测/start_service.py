import os
import sys
import subprocess

# 打印当前 Python 环境信息
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# 设置工作目录
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_infer_service'))
print(f"Working directory: {os.getcwd()}")

# 导入必要的模块
try:
    import fastapi
    import uvicorn
    print("Required modules are available")
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

# 设置知识库路径环境变量
kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloud_change_risk_assessment_kb.json')
os.environ['KNOWLEDGE_BASE_PATH'] = kb_path
print(f"Knowledge base path: {kb_path}")

# 启动服务
print("Starting AI inference service...")
try:
    # 直接导入并运行 main.py 中的应用
    sys.path.append(os.getcwd())
    from main import app
    
    # 使用 uvicorn 启动服务
    port = 8000  # 使用 8000 端口
    print(f"Starting service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
except Exception as e:
    print(f"Error starting service: {e}")
    sys.exit(1)