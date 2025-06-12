import os
import zipfile
import pandas as pd
import json

# 设置需要处理的根目录
root_dir = '/Users/heytea/Desktop/cursor/git 智能检测/datasets/GAIA/Companion_Data'
preview_file = 'data_preview.txt'

with open(preview_file, 'w', encoding='utf-8') as preview:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # 自动解压zip文件
            if filename.endswith('.zip'):
                unzip_dir = os.path.splitext(file_path)[0] + '_unzip'
                if not os.path.exists(unzip_dir):
                    os.makedirs(unzip_dir, exist_ok=True)
                    print(f'正在解压: {file_path} 到 {unzip_dir}')
                    preview.write(f'正在解压: {file_path} 到 {unzip_dir}\n')
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(unzip_dir)
            # 预览csv/json/txt文件内容
            elif filename.endswith('.csv'):
                print(f'预览CSV: {file_path}')
                preview.write(f'\n==== 预览CSV: {file_path} ====' + '\n')
                try:
                    df = pd.read_csv(file_path)
                    preview.write(df.head(10).to_string() + '\n')
                    print(df.head(10))
                except Exception as e:
                    preview.write(f'读取失败: {e}\n')
            elif filename.endswith('.json'):
                print(f'预览JSON: {file_path}')
                preview.write(f'\n==== 预览JSON: {file_path} ====' + '\n')
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f):
                            if i >= 10:
                                break
                            preview.write(line)
                            print(line.strip())
                except Exception as e:
                    preview.write(f'读取失败: {e}\n')
            elif filename.endswith('.txt'):
                print(f'预览TXT: {file_path}')
                preview.write(f'\n==== 预览TXT: {file_path} ====' + '\n')
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f):
                            if i >= 10:
                                break
                            preview.write(line)
                            print(line.strip())
                except Exception as e:
                    preview.write(f'读取失败: {e}\n')

print(f'数据预览已完成，详情见 {preview_file}') 