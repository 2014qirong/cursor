#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试基础模型功能
"""

import joblib
import os
import requests
import json

def test_basic_model():
    """测试基础模型"""
    print("🔍 测试基础模型...")
    
    model_path = '/Users/heytea/Desktop/cursor/git 智能检测/ai_infer_service/models/risk_clf.pkl'
    
    try:
        # 加载模型
        model = joblib.load(model_path)
        print(f"✅ 模型加载成功: {type(model)}")
        
        # 测试预测
        test_code = ["# 数据库连接池配置\nmax_connections: 50"]
        
        if hasattr(model, 'predict'):
            prediction = model.predict(test_code)
            print(f"📊 预测结果: {prediction}")
            
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(test_code)
            print(f"📊 概率结果: {proba}")
            
        return True
        
    except Exception as e:
        print(f"❌ 基础模型测试失败: {str(e)}")
        return False

def test_health_endpoint():
    """测试健康检查端点"""
    print("\n🔍 测试健康检查端点...")
    
    try:
        response = requests.get(
            "http://localhost:8001/health",
            timeout=5
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 健康检查成功!")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 健康检查异常: {str(e)}")
        return False

def test_simple_predict():
    """测试简单预测"""
    print("\n🔍 测试简单预测...")
    
    # 使用TEST_ECHO前缀来触发简单返回
    test_data = {
        "code": "# TEST_ECHO\n# 数据库连接池配置\npool:\n  max_connections: 50"
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/predict",
            json=test_data,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 简单预测成功!")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return True
        else:
            print(f"❌ 简单预测失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 简单预测异常: {str(e)}")
        return False

def check_knowledge_base():
    """检查知识库文件"""
    print("\n🔍 检查知识库文件...")
    
    kb_path = '/Users/heytea/Desktop/cursor/git 智能检测/cloud_change_risk_assessment_kb.json'
    
    try:
        if os.path.exists(kb_path):
            with open(kb_path, 'r') as f:
                kb = json.load(f)
            
            change_items = kb.get('change_items', [])
            print(f"✅ 知识库文件存在，包含 {len(change_items)} 条记录")
            
            if change_items:
                print(f"   示例记录类型: {change_items[0].get('type', 'unknown')}")
            
            return True
        else:
            print(f"❌ 知识库文件不存在: {kb_path}")
            return False
            
    except Exception as e:
        print(f"❌ 检查知识库异常: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== 基础模型测试 ===")
    
    results = {
        'basic_model': False,
        'health_check': False,
        'simple_predict': False,
        'knowledge_base': False
    }
    
    # 1. 测试基础模型
    results['basic_model'] = test_basic_model()
    
    # 2. 检查知识库
    results['knowledge_base'] = check_knowledge_base()
    
    # 3. 测试健康检查
    results['health_check'] = test_health_endpoint()
    
    # 4. 测试简单预测
    results['simple_predict'] = test_simple_predict()
    
    print("\n" + "="*50)
    print("📋 测试结果总结:")
    print(f"   🤖 基础模型: {'✅ 成功' if results['basic_model'] else '❌ 失败'}")
    print(f"   📚 知识库: {'✅ 成功' if results['knowledge_base'] else '❌ 失败'}")
    print(f"   💓 健康检查: {'✅ 成功' if results['health_check'] else '❌ 失败'}")
    print(f"   🔮 简单预测: {'✅ 成功' if results['simple_predict'] else '❌ 失败'}")
    
    success_count = sum(results.values())
    total_count = len(results)
    success_rate = (success_count / total_count) * 100
    
    print(f"\n📊 总体成功率: {success_count}/{total_count} ({success_rate:.1f}%)")
    
    if success_count >= 3:
        print("\n🎉 基础功能测试基本通过!")
    else:
        print("\n⚠️  基础功能存在问题，需要修复")