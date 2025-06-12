from zedx_processor import ZedxProcessor
import os

def main():
    # 获取数据目录
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'aiops2024')
    
    # 初始化处理器
    processor = ZedxProcessor(data_dir)
    
    # 构建知识库
    print("开始构建知识库...")
    processor.build_knowledge_base()
    print("知识库构建完成")

if __name__ == "__main__":
    main() 