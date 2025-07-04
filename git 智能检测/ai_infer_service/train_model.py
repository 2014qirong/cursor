import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os
import sys

class RiskClassifier:
    """风险分类器包装类，提供更好的接口"""
    
    def __init__(self, model):
        self.model = model
    
    def predict_proba(self, texts):
        """预测风险概率"""
        return self.model.predict_proba(texts)
    
    def predict(self, texts):
        """预测风险类别"""
        return self.model.predict(texts)

def train_and_save_model():
    try:
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

        # 特征提取
        vectorizer = TfidfVectorizer(max_features=1000)
        X = vectorizer.fit_transform(df['diff'])
        y = df['risk_level']

        print("创建模型管道...")
        # 创建模型管道
        pipe = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', LogisticRegression())
        ])

        print("训练模型...")
        # 训练模型
        pipe.fit(df['diff'], y)
        
        # 包装模型以提供更好的接口
        model = RiskClassifier(pipe)

        # 保存模型
        model_path = os.path.join(os.path.dirname(__file__), 'risk_clf.pkl')
        print(f"保存模型到: {model_path}")
        joblib.dump(model, model_path)
        
        print("模型训练和保存完成！")
        return True
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = train_and_save_model()
    sys.exit(0 if success else 1) 