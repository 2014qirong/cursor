import os
import json
import time
import argparse
from datetime import datetime

# 注意：需要先安装 OpenAI 库
# pip install openai
import openai

# 设置API密钥（注意不要将密钥硬编码在脚本中）
# openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_knowledge_base(num_patterns=10, categories=None, model="gpt-3.5-turbo"):
    """
    使用OpenAI API生成知识库数据
    
    Args:
        num_patterns: 要生成的风险模式数量
        categories: 风险类别列表，如果为None则使用默认类别
        model: 使用的OpenAI模型
    
    Returns:
        生成的知识库数据
    """
    if categories is None:
        categories = [
            "敏感信息暴露（密码、API密钥、证书等）", 
            "不安全的命令执行（命令注入、任意代码执行等）", 
            "容器和Kubernetes配置风险", 
            "权限和访问控制问题", 
            "SQL注入和数据访问风险"
        ]
    
    # 构建prompt
    prompt = f"""
    请你作为一位资深的代码安全分析专家和DevSecOps工程师，帮我生成一个代码风险知识库的内容。

    知识库需包含三个部分：
    1. risk_patterns：风险代码模式
    2. solutions：对应的解决方案
    3. abbreviations：相关缩写词解释

    请生成{num_patterns}条详细的风险模式和解决方案，涵盖以下类别（每类尽量平均分配）：
    {", ".join(categories)}

    每条风险模式请包含：
    - 具体的代码或配置片段（真实可信，有完整上下文）
    - 详细的风险描述
    - 风险来源（如"OWASP Top 10"、"CWE-数字"、"云原生安全最佳实践"等）

    每条解决方案请包含：
    - 具体的修复代码或配置（与风险模式对应）
    - 详细的修复建议和最佳实践
    - 来源（如官方文档、安全指南等）

    另外，请提供10个运维和安全领域常用的缩写词及其全称解释。

    所有内容请以JSON格式输出，符合以下结构：
    {{
      "risk_patterns": [
        {{
          "content": "具体的风险代码或配置片段",
          "description": "详细的风险描述",
          "source": "风险来源"
        }}
      ],
      "solutions": [
        {{
          "content": "具体的修复代码或配置片段",
          "description": "详细的修复建议",
          "source": "来源"
        }}
      ],
      "abbreviations": {{
        "缩写1": "全称1",
        "缩写2": "全称2"
      }}
    }}

    确保代码示例多样化，包括不同编程语言（Python、Java、JavaScript、Go等）和不同配置格式（YAML、JSON、XML等）。
    """

    # 使用API生成内容
    try:
        print(f"正在使用{model}生成{num_patterns}条风险模式...")
        
        # 对于API使用，请取消以下注释并确保设置了API密钥
        """
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一位安全专家，擅长识别代码和配置中的安全风险。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        content = response.choices[0].message.content
        """
        
        # 临时替代方案：模拟响应（真实使用时请用上面的API调用）
        print("请注意：此为模拟生成，实际使用时请取消对API调用的注释")
        time.sleep(2)
        content = """
        {
          "risk_patterns": [
            {
              "content": "# Config file for database access\nDB_PASSWORD = \"supersecret123\"\nAPI_KEY = \"abcdef123456\"\n\ndef connect_to_database():\n    connection = DatabaseClient(\n        host=\"db.example.com\",\n        username=\"admin\",\n        password=DB_PASSWORD,\n        api_key=API_KEY\n    )\n    return connection",
              "description": "代码中直接硬编码了数据库密码和API密钥，这些敏感信息可能会被提交到版本控制系统，导致凭证泄露",
              "source": "OWASP Top 10 2021: A07 - Identification and Authentication Failures"
            }
          ],
          "solutions": [
            {
              "content": "# Config file for database access\nimport os\nfrom dotenv import load_dotenv\n\n# 从环境变量加载敏感信息\nload_dotenv()\nDB_PASSWORD = os.environ.get(\"DB_PASSWORD\")\nAPI_KEY = os.environ.get(\"API_KEY\")\n\ndef connect_to_database():\n    connection = DatabaseClient(\n        host=\"db.example.com\",\n        username=\"admin\",\n        password=DB_PASSWORD,\n        api_key=API_KEY\n    )\n    return connection",
              "description": "使用环境变量或密钥管理服务存储敏感信息，避免在代码中硬编码凭证。可以使用.env文件配合.gitignore确保不会将敏感信息提交到版本控制系统",
              "source": "OWASP Security Cheat Sheet: Password Storage"
            }
          ],
          "abbreviations": {
            "CVE": "Common Vulnerabilities and Exposures",
            "CSRF": "Cross-Site Request Forgery",
            "XSS": "Cross-Site Scripting"
          }
        }
        """
        
        # 解析JSON内容
        try:
            result = json.loads(content)
            
            # 检查并修复可能的格式问题
            if not isinstance(result, dict):
                print("生成的内容不是有效的JSON对象，将尝试修复")
                result = {"risk_patterns": [], "solutions": [], "abbreviations": {}}
            
            if "risk_patterns" not in result:
                result["risk_patterns"] = []
            if "solutions" not in result:
                result["solutions"] = []
            if "abbreviations" not in result:
                result["abbreviations"] = {}
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"llm_kb_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"生成完成! 结果已保存到: {output_file}")
            print(f"风险模式总数: {len(result['risk_patterns'])}")
            print(f"解决方案总数: {len(result['solutions'])}")
            print(f"缩略语总数: {len(result['abbreviations'])}")
            
            return result
            
        except json.JSONDecodeError:
            print("生成的内容不是有效的JSON格式")
            print("原始内容：", content[:500])  # 打印部分内容用于调试
            return None
            
    except Exception as e:
        print(f"生成知识库时出错: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="生成代码风险知识库")
    parser.add_argument("--num", type=int, default=10, help="要生成的风险模式数量")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="使用的模型")
    parser.add_argument("--api_key", type=str, help="OpenAI API密钥")
    args = parser.parse_args()
    
    if args.api_key:
        openai.api_key = args.api_key
    
    generate_knowledge_base(num_patterns=args.num, model=args.model)

if __name__ == "__main__":
    main() 