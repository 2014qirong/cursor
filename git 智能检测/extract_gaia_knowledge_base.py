import pandas as pd
import json

# 读取 GAIA 数据集
input_file = 'gaia_dataset.csv'  # 请根据实际文件名修改
output_file = 'knowledge_base.json'

# 读取数据
print(f"正在读取数据集: {input_file}")
df = pd.read_csv(input_file)

risk_patterns = []
solutions = []

for _, row in df.iterrows():
    # 只提取高风险或高危（支持多种写法）
    risk = str(row.get('risk_level', '')).strip()
    if risk in ['高风险', '高危', '1', 'high', 'HIGH']:
        # 提取风险模式
        content = str(row.get('content', '')).strip()
        if content:
            risk_patterns.append({
                "content": content,
                "source": "GAIA-DataSet"
            })
        # 提取解决方案
        solution = str(row.get('solution', '')).strip()
        if solution:
            solutions.append({
                "content": solution,
                "source": "GAIA-DataSet"
            })

knowledge_base = {
    "risk_patterns": risk_patterns,
    "solutions": solutions,
    "abbreviations": {}
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(knowledge_base, f, ensure_ascii=False, indent=2)

print(f"知识库提取完成，已保存为 {output_file}") 