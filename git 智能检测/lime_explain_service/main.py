from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from lime.lime_text import LimeTextExplainer
import requests
import json
from typing import Dict, Any, List, Tuple
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import re

# 导入 Prometheus 客户端库
# from prometheus_client import start_http_server, Counter

app = FastAPI(title="LIME解释服务")

# 模型文件路径
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'risk_clf.pkl')

# 加载模型和解释器
try:
    model = joblib.load(MODEL_PATH)
    explainer = LimeTextExplainer(class_names=["低危", "高危"])
except FileNotFoundError:
    raise FileNotFoundError(f"未找到模型文件: {MODEL_PATH}")

# 请求模型
class DiffRequest(BaseModel):
    diff_content: str

# 解释结果模型
class ExplanationItem(BaseModel):
    feature: str
    weight: float

# 响应模型
class ExplainResponse(BaseModel):
    explanation: List[Tuple[str, float]]

# 定义 Prometheus 指标
# Counter 指标用于记录 LIME 解释事件的次数
# LIME_EXPLANATION_EVENTS = Counter(
#     'lime_explanation_event_total',
#     'Total number of LIME explanation events',
#     ['risk_level']
# )

# InfluxDB 配置从环境变量获取
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw==")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "risk_assessment")

# 初始化 InfluxDB 客户端
try:
    client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print("InfluxDB client initialized.")
except Exception as e:
    print(f"Error initializing InfluxDB client: {e}")
    client = None
    write_api = None

@app.on_event("startup")
async def startup_event():
    global model, explainer, client, write_api
    try:
        model = joblib.load(MODEL_PATH)
        explainer = LimeTextExplainer(class_names=["低危", "高危"])
        print("模型和解释器加载成功")
    except FileNotFoundError:
        print(f"未找到模型文件: {MODEL_PATH}")
        raise FileNotFoundError(f"未找到模型文件: {MODEL_PATH}")

    # 重新初始化 InfluxDB 客户端 (如果在全局初始化时失败)
    if client is None or write_api is None:
        try:
            client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            print("InfluxDB client initialized during startup.")
        except Exception as e:
            print(f"Error initializing InfluxDB client during startup: {e}")

@app.post("/explain")
async def explain_risk(request: DiffRequest):
    try:
        # 生成解释
        exp = explainer.explain_instance(request.diff_content, model.predict_proba, num_features=5)
        explanation = exp.as_list()
        
        # 假设我们知道这个 diff 对应的是高危还是低危，这里简化为高危事件
        # 实际中您需要根据预测服务的输出或其他方式确定风险等级
        associated_risk_level = "高危" # 替换为实际获取的风险等级

        # 增加 LIME 解释事件计数
        # LIME_EXPLANATION_EVENTS.labels(risk_level=associated_risk_level).inc()
        
        # 预处理文本 (这里简单地移除标点符号和转换为小写)
        processed_text = re.sub(r'[^\w\s]', '', request.diff_content).lower()

        # 生成解释
        explanation = explainer.explain_instance(
            processed_text,
            lambda x: model.predict_proba(x),
            num_features=5  # 明确设置特征数量
        )

        # 获取解释结果 (例如，作为 HTML 或文本)
        explanation_html = explanation.as_html() # 保留HTML用于API响应
        explanation_list = explanation.as_list() # 获取列表形式用于InfluxDB

        # 写入数据到 InfluxDB
        if write_api:
            try:
                # 将 explanation.as_list() 转换成字符串写入
                explanation_list_str = str(explanation_list)
                point = influxdb_client.Point("lime_explanations") \
                    .tag("host", "localhost") \
                    .field("explanation", explanation_list_str)
                write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
                print(f"写入 InfluxDB 成功: explanation={explanation_list_str[:100]}...") # 打印部分内容以避免过长输出
            except Exception as e:
                print(f"写入 InfluxDB 失败: {e}")

        # 返回HTML解释作为API响应
        return {"explanation": explanation_html}
    except Exception as e:
        print(f"解释失败: {e}")
        return {"error": str(e)}

@app.get("/health")
def health_check():
    """
    健康检查端点
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 