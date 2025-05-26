import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# 1. 读取数据
csv_path = './commit_diffs_labeled.csv'
# 脚本所在的当前目录是 project-backend/app/ml/
# 数据文件在项目根目录，所以需要向上两级
csv_path = os.path.join(os.path.dirname(__file__), '..', '..', csv_path)

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"未找到训练数据: {csv_path}")
df = pd.read_csv(csv_path)
X = df['diff']
y = df['label'].map({'高危': 1, '低危': 0})

# 2. 划分训练/测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 构建pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=2000)),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# 4. 训练
pipeline.fit(X_train, y_train)

# 5. 评估
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# 6. 保存模型
model_dir = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'risk_clf.pkl')
joblib.dump(pipeline, model_path)
print(f'模型已保存到 {model_path}') 