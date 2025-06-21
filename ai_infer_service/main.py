from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import traceback

app = FastAPI()

# 路径设置
KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')

# InfluxDB 配置
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "A__zIBb1iT9wWi6lN4VqIlNcADsOmmCp4WRfx0pzPAw8YO8WFeJCEKi24G2IovwP4Ooj4dZt9wjjK53kkZNysw=="
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "risk_assessment"

# 初始化 InfluxDB 客户端
try:
    print(f"连接 InfluxDB: {INFLUXDB_URL}")
    client = influxdb_client.InfluxDBClient(
        url=INFLUXDB_URL,
        token=INFLUXDB_TOKEN,
        org=INFLUXDB_ORG
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print("InfluxDB 客户端初始化成功")
except Exception as e:
    print(f"InfluxDB 客户端初始化失败: {str(e)}")
    client = None
    write_api = None

# 加载知识库
def load_knowledge_base(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载知识库失败: {str(e)}")
        # 返回空知识库
        return {"risk_patterns": [], "solutions": [], "abbreviations": {}}

# 训练模型
def train_model():
    print("开始训练模型...")
    
    # 示例训练数据
    data = {
        'diff': [
            '直接暴露密码: supersecret123',
            '添加资源限制: cpu: 250m, memory: 500m',
            '暴露敏感配置: DB_PASSWORD=supersecret123',
            '添加资源限制: cpu: 500m, memory: 1Gi',
            '直接暴露密钥: secretKeyRef: supersecret123',
            '添加资源限制: cpu: 100m, memory: 200m',
            '暴露敏感配置: API_KEY=abcdef123456',
            '添加资源限制: cpu: 300m, memory: 600m',
            '直接暴露密码: PASSWORD=supersecret123',
            '添加资源限制: cpu: 400m, memory: 800m',
            'import os\nos.system("rm -rf /")',
            'def execute_command(cmd):\n    import subprocess\n    return subprocess.check_output(cmd, shell=True)',
            'def safe_function(a, b):\n    return a + b'
        ],
        'risk_level': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0]  # 1表示高风险，0表示低风险
    }

    # 创建DataFrame
    df = pd.DataFrame(data)

    print("创建模型管道...")
    # 创建模型管道
    model = Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=1000)),
        ('classifier', LogisticRegression())
    ])

    print("训练模型...")
    # 训练模型
    model.fit(df['diff'], df['risk_level'])
    
    print("模型训练完成")
    return model

# 创建向量化器和准备向量
def prepare_vectors(knowledge_base):
    vectorizer = TfidfVectorizer()
    
    # 准备风险模式文档
    risk_docs = [pattern['content'] for pattern in knowledge_base['risk_patterns']]
    if risk_docs:
        risk_vectors = vectorizer.fit_transform(risk_docs)
    else:
        risk_vectors = None
    
    # 准备解决方案文档
    solution_docs = [sol['content'] for sol in knowledge_base['solutions']]
    if solution_docs and risk_vectors is not None:
        solution_vectors = vectorizer.transform(solution_docs)
    else:
        solution_vectors = None
    
    return vectorizer, risk_vectors, solution_vectors

# 向 InfluxDB 写入数据
def write_to_influxdb(data, measurement="risk_assessment"):
    if write_api is None:
        print("InfluxDB 客户端未初始化，无法写入数据")
        return False
    
    try:
        # 创建数据点
        point = influxdb_client.Point(measurement)
        
        # 添加字段
        for key, value in data.items():
            if isinstance(value, (int, float, bool, str)):
                point = point.field(key, value)
            elif isinstance(value, dict):
                # 将字典转换为字符串
                point = point.field(key, str(value))
        
        # 写入数据
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"数据成功写入 InfluxDB: {data}")
        return True
    except Exception as e:
        print(f"写入 InfluxDB 失败: {str(e)}")
        traceback.print_exc()
        return False

# 初始化资源
try:
    print("加载知识库...")
    knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_PATH)
    vectorizer, risk_vectors, solution_vectors = prepare_vectors(knowledge_base)
    print("知识库加载成功")
    
    print("训练模型...")
    model = train_model()
    print("模型训练成功")
except Exception as e:
    print(f"初始化错误: {str(e)}")
    # 如果加载失败，使用默认值
    knowledge_base = {"risk_patterns": [], "solutions": [], "abbreviations": {}}
    vectorizer = TfidfVectorizer()
    risk_vectors = None
    solution_vectors = None
    model = Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=1000)),
        ('classifier', LogisticRegression())
    ])

class CodeInput(BaseModel):
    code: str

def get_risk_level(prob: float) -> str:
    """获取风险等级"""
    if prob >= 0.7:
        return "高风险"
    elif prob >= 0.5:
        return "中风险"
    else:
        return "低风险"

def combine_probabilities(base_prob: float, pattern_sim: float) -> float:
    """综合概率计算"""
    # 使用加权平均
    w1, w2 = 0.7, 0.3  # 权重可调
    return w1 * base_prob + w2 * pattern_sim

@app.post("/predict")
async def predict(input: CodeInput):
    try:
        code = input.code
        
        # 基础模型预测
        try:
            base_prob = float(model.predict_proba([code])[0][1])  # 获取正类的概率
        except Exception as e:
            print(f"基础模型预测错误: {str(e)}")
            base_prob = 0.5  # 如果基础模型预测失败，使用默认值
        
        # 知识库匹配
        matched_pattern = None
        suggested_solution = None
        max_risk_sim = 0.0
        
        if risk_vectors is not None:
            try:
                code_vector = vectorizer.transform([code])
                
                # 计算与风险模式的相似度
                risk_similarities = cosine_similarity(code_vector, risk_vectors)[0]
                if len(risk_similarities) > 0:
                    max_risk_sim = max(risk_similarities)
                    risk_index = np.argmax(risk_similarities)
                    matched_pattern = knowledge_base['risk_patterns'][risk_index]
                
                # 获取相关的解决方案
                if solution_vectors is not None and len(solution_vectors.toarray()) > 0:
                    solution_similarities = cosine_similarity(code_vector, solution_vectors)[0]
                    if len(solution_similarities) > 0:
                        solution_index = np.argmax(solution_similarities)
                        suggested_solution = knowledge_base['solutions'][solution_index]
            except Exception as e:
                print(f"知识库匹配错误: {str(e)}")
        
        # 综合评估
        if matched_pattern:
            enhanced_prob = combine_probabilities(base_prob, max_risk_sim)
        else:
            enhanced_prob = base_prob
        
        risk_level = get_risk_level(enhanced_prob)
        
        # 生成解释说明
        if risk_level == "高风险":
            if matched_pattern:
                explanation = f"模型判定为高风险，原因：代码与知识库高风险模式（如：{matched_pattern['content'][:20]}...）相似度高，且模型概率为{enhanced_prob:.2f}。"
            else:
                explanation = f"模型判定为高风险，原因：模型概率为{enhanced_prob:.2f}，但未命中知识库高风险模式。"
        elif risk_level == "中风险":
            if matched_pattern:
                explanation = f"模型判定为中风险，原因：代码与知识库风险模式（如：{matched_pattern['content'][:20]}...）有一定相似度，模型概率为{enhanced_prob:.2f}。"
            else:
                explanation = f"模型判定为中风险，原因：模型概率为{enhanced_prob:.2f}，但未命中知识库风险模式。"
        else:
            explanation = f"模型判定为低风险，原因：代码未检测到敏感信息，且与高风险模式相似度低，模型概率为{enhanced_prob:.2f}。"
        
        result = {
            'probability': float(enhanced_prob),  # 确保概率值是 float 类型
            'risk_level': risk_level,
            'explanation': explanation
        }
        
        if matched_pattern:
            result['matched_pattern'] = matched_pattern
        if suggested_solution:
            result['suggested_solution'] = suggested_solution
        
        # 写入 InfluxDB
        influxdb_data = {
            'probability': result['probability'],
            'risk_level': result['risk_level'],
            'explanation': result['explanation'],
            'code_sample': code[:100]  # 仅存储代码的前100个字符
        }
        
        if matched_pattern:
            influxdb_data['matched_pattern'] = matched_pattern['content']
            influxdb_data['pattern_source'] = matched_pattern['source']
        
        if suggested_solution:
            influxdb_data['solution'] = suggested_solution['content']
            influxdb_data['solution_source'] = suggested_solution['source']
        
        write_to_influxdb(influxdb_data)
        
        return result
    except Exception as e:
        print(f"预测错误: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain")
async def explain(input: CodeInput):
    try:
        # 获取预测结果
        prediction = await predict(input)
        
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
        
        # 查找相关缩略语
        relevant_abbreviations = {}
        for abbr, full in knowledge_base['abbreviations'].items():
            if abbr in input.code:
                relevant_abbreviations[abbr] = full
        
        explanation['relevant_abbreviations'] = relevant_abbreviations
        
        # 写入 InfluxDB
        write_to_influxdb({
            'explanation': str(explanation),
            'code_sample': input.code[:100]
        }, measurement="risk_explanation")
        
        return explanation
    except Exception as e:
        print(f"解释错误: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """健康检查端点"""
    health_status = {
        "status": "healthy",
        "influxdb_connected": client is not None and write_api is not None,
        "model_loaded": model is not None,
        "knowledge_base_loaded": knowledge_base is not None
    }
    return health_status 