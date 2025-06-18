#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_ack_webhook():
    """测试阿里云 ACK 节点池变更的 GitLab Webhook 端点"""
    
    # 读取测试数据
    try:
        with open('gitlab_ack_push_event.json', 'r') as f:
            webhook_payload = json.load(f)
        print("✅ 成功加载测试数据")
    except Exception as e:
        print(f"❌ 加载测试数据失败: {e}")
        return False
    
    # 测试不同的端口
    test_ports = [8001, 8002, 8000]
    
    for port in test_ports:
        url = f"http://127.0.0.1:{port}/gitlab-webhook"
        print(f"\n=== 测试端口 {port} ===")
        
        try:
            # 发送 POST 请求
            response = requests.post(
                url,
                json=webhook_payload,
                headers={'Content-Type': 'application/json'},
                timeout=30  # 增加超时时间，因为风险评估可能需要更长时间
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ GitLab Webhook 测试成功！")
                print("\n=== 风险评估结果 ===")
                print(f"项目: {result.get('project_name', 'unknown')}")
                print(f"处理的提交数: {result.get('processed_commits', 0)}")
                
                # 打印每个提交的风险评估结果
                risk_assessments = result.get('risk_assessments', [])
                for i, assessment in enumerate(risk_assessments):
                    print(f"\n提交 {i+1}: {assessment.get('commit_id', 'unknown')[:8]}")
                    print(f"作者: {assessment.get('commit_author', 'unknown')}")
                    print(f"消息: {assessment.get('commit_message', 'unknown')[:50]}...")
                    print(f"风险等级: {assessment.get('risk_level', 'unknown')}")
                    print(f"风险概率: {assessment.get('probability', 0)}")
                    
                    # 打印匹配的风险模式
                    matched_pattern = assessment.get('matched_pattern', {})
                    if matched_pattern:
                        print(f"\n匹配的风险模式:")
                        print(f"内容: {matched_pattern.get('content', 'unknown')[:100]}...")
                        print(f"来源: {matched_pattern.get('source', 'unknown')}")
                        
                        # 打印关键指标
                        key_metrics = matched_pattern.get('key_metrics_to_monitor', [])
                        if key_metrics:
                            print(f"\n关键监控指标:")
                            for metric in key_metrics[:3]:  # 只打印前3个
                                print(f"- {metric}")
                        
                        # 打印潜在影响
                        impacts = matched_pattern.get('potential_impacts', [])
                        if impacts:
                            print(f"\n潜在影响:")
                            for impact in impacts[:3]:  # 只打印前3个
                                print(f"- {impact}")
                        
                        # 打印缓解策略
                        strategies = matched_pattern.get('mitigation_strategies', [])
                        if strategies:
                            print(f"\n缓解策略:")
                            for strategy in strategies[:3]:  # 只打印前3个
                                print(f"- {strategy}")
                
                return True
            else:
                print(f"❌ 请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 无法连接到端口 {port}")
        except requests.exceptions.Timeout:
            print(f"❌ 请求超时")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    print("\n❌ 所有端口测试失败")
    return False

def test_health_endpoint():
    """测试健康检查端点"""
    test_ports = [8001, 8002, 8000]
    
    for port in test_ports:
        url = f"http://127.0.0.1:{port}/health"
        print(f"\n=== 测试健康检查端口 {port} ===")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                print("✅ 健康检查成功！")
                return port
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 无法连接到端口 {port}")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    return None

if __name__ == '__main__':
    print("=== 阿里云 ACK 节点池变更风险评估测试 ===\n")
    
    # 先测试健康检查
    working_port = test_health_endpoint()
    if working_port:
        print(f"\n服务运行正常（端口 {working_port}），开始测试 GitLab Webhook...")
        test_ack_webhook()
    else:
        print("\n❌ 服务未运行，请先启动 AI 推理服务")
        print("提示: 在 ai_infer_service 目录下运行 'python main.py'")