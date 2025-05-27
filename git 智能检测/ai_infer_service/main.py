from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import requests
import json
import numpy as np
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

app = FastAPI()

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'risk_clf.pkl')

# InfluxDB 配置占位符
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "z93DtbjAJLbms5UU13x6o7PxEBLIFDaDEZ5fAniMGXdJorIvGQGvmFC8b3xQWTRvdcFx8gV_mELEDm8WtbS3lQ=="
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "risk_assessment"

# 初始化 InfluxDB 客户端
try:
    client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print("InfluxDB client initialized.")
except Exception as e:
    print(f"Error initializing InfluxDB client: {e}")
    client = None
    write_api = None

# 加载模型
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"未找到模型文件: {MODEL_PATH}")

class DiffRequest(BaseModel):
    diff_content: str

@app.on_event("startup")
async def startup_event():
    global model, client, write_api
    try:
        model = joblib.load(MODEL_PATH)
        print("模型加载成功")
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

@app.post("/predict")
async def predict_risk(request: DiffRequest):
    try:
        # 预测风险等级
        prediction = model.predict([request.diff_content])
        prob = model.predict_proba([request.diff_content])[0]
        risk_level = "高危" if prediction[0] == 1 else "低危"
        
        # 写入数据到 InfluxDB
        if write_api:
            try:
                # 写入风险预测概率
                point = influxdb_client.Point("risk_assessment") \
                    .tag("host", "localhost") \
                    .field("probability", float(prob[1]))
                write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
                print(f"写入 InfluxDB 成功: probability={prob[1]}")
            except Exception as e:
                print(f"写入 InfluxDB 失败: {e}")
        
        return {"risk_level": risk_level, "prob": prob.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """
    健康检查端点
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 