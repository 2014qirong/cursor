import json
import os
import glob

def merge_knowledge_bases(input_files, output_file="knowledge_base.json"):
    """
    合并多个知识库JSON文件到一个最终文件
    
    Args:
        input_files: 输入文件路径列表
        output_file: 输出文件路径
    """
    result = {
        "risk_patterns": [],
        "solutions": [],
        "abbreviations": {}
    }
    
    for file_path in input_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 合并风险模式
                if "risk_patterns" in data and isinstance(data["risk_patterns"], list):
                    result["risk_patterns"].extend(data["risk_patterns"])
                
                # 合并解决方案
                if "solutions" in data and isinstance(data["solutions"], list):
                    result["solutions"].extend(data["solutions"])
                
                # 合并缩略语
                if "abbreviations" in data and isinstance(data["abbreviations"], dict):
                    result["abbreviations"].update(data["abbreviations"])
                    
            print(f"成功合并: {file_path}")
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
    
    # 去重（根据内容）
    unique_patterns = []
    seen_patterns = set()
    for pattern in result["risk_patterns"]:
        content = pattern.get("content", "")
        if content and content not in seen_patterns:
            seen_patterns.add(content)
            unique_patterns.append(pattern)
    result["risk_patterns"] = unique_patterns
    
    # 解决方案去重
    unique_solutions = []
    seen_solutions = set()
    for solution in result["solutions"]:
        content = solution.get("content", "")
        if content and content not in seen_solutions:
            seen_solutions.add(content)
            unique_solutions.append(solution)
    result["solutions"] = unique_solutions
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"合并完成! 结果已保存到: {output_file}")
    print(f"风险模式总数: {len(result['risk_patterns'])}")
    print(f"解决方案总数: {len(result['solutions'])}")
    print(f"缩略语总数: {len(result['abbreviations'])}")
    
    return result

def main():
    # 获取当前目录下所有llm_kb_*.json文件
    input_files = glob.glob("llm_kb_*.json")
    
    if not input_files:
        print("未找到符合llm_kb_*.json格式的文件！")
        return
    
    merge_knowledge_bases(input_files)

if __name__ == "__main__":
    main() 