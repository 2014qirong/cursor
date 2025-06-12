import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os
import sys

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

        print("创建模型管道...")
        # 创建模型管道
        model = Pipeline([
            ('vectorizer', TfidfVectorizer(max_features=1000)),
            ('classifier', LogisticRegression())
        ])

        print("训练模型...")
        # 训练模型
        model.fit(df['diff'], df['risk_level'])

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