import os
import json
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple
import chardet

class ZedxProcessor:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.knowledge_base = {
            'risk_patterns': [],
            'solutions': [],
            'abbreviations': {}
        }
    
    def _read_file_with_encoding(self, file_path: str) -> str:
        """使用正确的编码读取文件"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            # 如果检测到的编码不正确，尝试其他常见编码
            for encoding in ['gbk', 'gb2312', 'gb18030', 'utf-16']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
            raise UnicodeDecodeError(f"无法找到正确的编码来读取文件: {file_path}")
    
    def process_zedx_file(self, file_path: str) -> Dict:
        """处理单个 ZEDX 文件"""
        temp_dir = f"temp_{os.path.basename(file_path)}"
        
        # 解压 ZEDX 文件
        with zipfile.ZipFile(file_path.replace('.zedx', '.zip'), 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # 解析文档结构
        tree = ET.parse(f"{temp_dir}/nodetree.xml")
        root = tree.getroot()
        
        # 提取知识
        knowledge = {
            'risk_patterns': self._extract_risk_patterns(temp_dir),
            'solutions': self._extract_solutions(temp_dir),
            'abbreviations': self._parse_abbreviations(f"{temp_dir}/documents/log.html")
        }
        
        # 清理临时目录
        os.system(f"rm -rf {temp_dir}")
        return knowledge
    
    def _extract_risk_patterns(self, doc_dir: str) -> List[Dict]:
        """提取风险模式"""
        patterns = []
        # 遍历文档目录
        for root, _, files in os.walk(f"{doc_dir}/documents"):
            for file in files:
                if file.endswith('.html'):
                    try:
                        content = self._read_file_with_encoding(os.path.join(root, file))
                        # 提取风险相关内容
                        if '风险' in content or '故障' in content or '错误' in content:
                            patterns.append({
                                'source': file,
                                'content': content,
                                'keywords': self._extract_keywords(content)
                            })
                    except Exception as e:
                        print(f"处理文件时出错 {file}: {str(e)}")
        return patterns
    
    def _extract_solutions(self, doc_dir: str) -> List[Dict]:
        """提取解决方案"""
        solutions = []
        for root, _, files in os.walk(f"{doc_dir}/documents"):
            for file in files:
                if file.endswith('.html'):
                    try:
                        content = self._read_file_with_encoding(os.path.join(root, file))
                        # 提取解决方案相关内容
                        if '解决方案' in content or '处理方法' in content:
                            solutions.append({
                                'source': file,
                                'content': content,
                                'keywords': self._extract_keywords(content)
                            })
                    except Exception as e:
                        print(f"处理文件时出错 {file}: {str(e)}")
        return solutions
    
    def _parse_abbreviations(self, log_file: str) -> Dict[str, str]:
        """解析缩略语"""
        abbreviations = {}
        if os.path.exists(log_file):
            try:
                content = self._read_file_with_encoding(log_file)
                # 解析缩略语定义
                # 实现缩略语提取逻辑
            except Exception as e:
                print(f"处理缩略语文件时出错: {str(e)}")
        return abbreviations
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        # 实现关键词提取逻辑
        return []
    
    def build_knowledge_base(self):
        """构建知识库"""
        for file in os.listdir(self.data_dir):
            if file.endswith('.zedx'):
                try:
                    print(f"处理文件: {file}")
                    knowledge = self.process_zedx_file(os.path.join(self.data_dir, file))
                    # 整合知识
                    self.knowledge_base['risk_patterns'].extend(knowledge['risk_patterns'])
                    self.knowledge_base['solutions'].extend(knowledge['solutions'])
                    self.knowledge_base['abbreviations'].update(knowledge['abbreviations'])
                except Exception as e:
                    print(f"处理文件时出错 {file}: {str(e)}")
        
        # 保存知识库
        with open('knowledge_base.json', 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2) 