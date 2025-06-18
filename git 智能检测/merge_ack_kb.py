#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def merge_knowledge_bases():
    """将阿里云 ACK 节点池变更的风险评估知识库条目合并到现有的知识库中"""
    
    # 加载现有的知识库
    try:
        with open('cloud_change_risk_assessment_kb.json', 'r', encoding='utf-8') as f:
            main_kb = json.load(f)
        print(f"✅ 成功加载主知识库，包含 {len(main_kb.get('change_items', []))} 条记录")
    except Exception as e:
        print(f"❌ 加载主知识库失败: {e}")
        return False
    
    # 加载阿里云 ACK 节点池变更的知识库
    try:
        with open('alicloud_ack_nodepool_kb.json', 'r', encoding='utf-8') as f:
            ack_kb = json.load(f)
        print(f"✅ 成功加载 ACK 节点池知识库，包含 {len(ack_kb.get('change_items', []))} 条记录")
    except Exception as e:
        print(f"❌ 加载 ACK 节点池知识库失败: {e}")
        return False
    
    # 检查是否已存在相同类型的条目
    existing_types = [item.get('type') for item in main_kb.get('change_items', [])]
    new_items = []
    
    for item in ack_kb.get('change_items', []):
        item_type = item.get('type')
        if item_type in existing_types:
            print(f"⚠️ 知识库中已存在类型为 {item_type} 的条目，将更新")
            # 更新现有条目
            for i, existing_item in enumerate(main_kb['change_items']):
                if existing_item.get('type') == item_type:
                    main_kb['change_items'][i] = item
                    break
        else:
            print(f"✅ 添加新条目: {item_type}")
            new_items.append(item)
    
    # 添加新条目
    main_kb['change_items'].extend(new_items)
    
    # 保存更新后的知识库
    try:
        # 备份原始知识库
        backup_path = 'cloud_change_risk_assessment_kb.backup.json'
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(main_kb, f, ensure_ascii=False, indent=2)
        print(f"✅ 已备份原始知识库到 {backup_path}")
        
        # 保存更新后的知识库
        with open('cloud_change_risk_assessment_kb.json', 'w', encoding='utf-8') as f:
            json.dump(main_kb, f, ensure_ascii=False, indent=2)
        print(f"✅ 成功更新知识库，现包含 {len(main_kb.get('change_items', []))} 条记录")
        return True
    except Exception as e:
        print(f"❌ 保存知识库失败: {e}")
        return False

if __name__ == '__main__':
    print("=== 合并阿里云 ACK 节点池变更风险评估知识库 ===\n")
    merge_knowledge_bases()