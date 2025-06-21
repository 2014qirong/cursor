#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云 WAF API 高风险变更操作脚本
参考文档: https://cloud.tencent.com/document/api/627/53618
变更类型: 生产环境WAF安全策略紧急调整
风险等级: CRITICAL
"""

import json
import time
import hashlib
import hmac
import base64
from datetime import datetime
import requests
import os
from typing import Dict, List, Any

class TencentWAFAPI:
    """
    腾讯云 WAF API 操作类
    实现高风险WAF配置变更操作
    """
    
    def __init__(self):
        # 从环境变量获取认证信息
        self.secret_id = os.getenv('TENCENT_SECRET_ID', '${TENCENT_SECRET_ID}')
        self.secret_key = os.getenv('TENCENT_SECRET_KEY', '${TENCENT_SECRET_KEY}')
        self.region = os.getenv('TENCENT_REGION', 'ap-guangzhou')
        self.endpoint = 'waf.tencentcloudapi.com'
        self.service = 'waf'
        self.version = '2018-01-25'
        
        # WAF实例配置
        self.instance_id = os.getenv('WAF_INSTANCE_ID', '${WAF_INSTANCE_ID}')
        self.domain = os.getenv('PRODUCTION_DOMAIN', '${PRODUCTION_DOMAIN}')
        
        # 变更记录
        self.change_log = []
        
    def _sign_request(self, method: str, uri: str, query: str, headers: Dict[str, str], payload: str) -> str:
        """
        腾讯云API签名算法 TC3-HMAC-SHA256
        """
        algorithm = 'TC3-HMAC-SHA256'
        timestamp = str(int(time.time()))
        date = datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
        
        # 步骤 1：拼接规范请求串
        http_request_method = method
        canonical_uri = uri
        canonical_querystring = query
        canonical_headers = '\n'.join([f'{k.lower()}:{v}' for k, v in sorted(headers.items())]) + '\n'
        signed_headers = ';'.join([k.lower() for k in sorted(headers.keys())])
        hashed_request_payload = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        canonical_request = f'{http_request_method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{hashed_request_payload}'
        
        # 步骤 2：拼接待签名字符串
        credential_scope = f'{date}/{self.service}/tc3_request'
        hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        string_to_sign = f'{algorithm}\n{timestamp}\n{credential_scope}\n{hashed_canonical_request}'
        
        # 步骤 3：计算签名
        secret_date = hmac.new(f'TC3{self.secret_key}'.encode('utf-8'), date.encode('utf-8'), hashlib.sha256).digest()
        secret_service = hmac.new(secret_date, self.service.encode('utf-8'), hashlib.sha256).digest()
        secret_signing = hmac.new(secret_service, 'tc3_request'.encode('utf-8'), hashlib.sha256).digest()
        signature = hmac.new(secret_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # 步骤 4：拼接 Authorization
        authorization = f'{algorithm} Credential={self.secret_id}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
        
        return authorization, timestamp
    
    def _make_request(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送API请求
        """
        url = f'https://{self.endpoint}'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Host': self.endpoint,
            'X-TC-Action': action,
            'X-TC-Version': self.version,
            'X-TC-Region': self.region
        }
        
        payload = json.dumps(params)
        authorization, timestamp = self._sign_request('POST', '/', '', headers, payload)
        
        headers['Authorization'] = authorization
        headers['X-TC-Timestamp'] = timestamp
        
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=30)
            result = response.json()
            
            # 记录变更日志
            self.change_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'params': params,
                'response': result,
                'status': 'success' if response.status_code == 200 else 'failed'
            })
            
            return result
        except Exception as e:
            error_result = {'Error': {'Code': 'RequestError', 'Message': str(e)}}
            self.change_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'params': params,
                'response': error_result,
                'status': 'error'
            })
            return error_result
    
    def create_critical_whitelist_rule(self) -> Dict[str, Any]:
        """
        创建极高风险的全网IP白名单规则
        API: AddDomainWhiteRule
        风险等级: CRITICAL
        """
        print("🚨 执行CRITICAL风险操作: 创建全网IP白名单规则")
        
        params = {
            'Domain': self.domain,
            'Rules': [
                {
                    'Id': 1,
                    'WhiteRuleType': 1,  # IP白名单
                    'Src': '0.0.0.0/0',  # 危险：允许所有IP
                    'Status': 1,  # 启用
                    'MatchField': 'IP',
                    'MatchMethod': 'equal',
                    'MatchContent': '0.0.0.0/0',
                    'RuleName': '紧急全网白名单-生产环境',
                    'RuleAction': 'allow',
                    'ValidTime': 3600,  # 1小时有效期
                    'JobType': 'add',
                    'JobDateTime': int(time.time()) + 60,  # 1分钟后生效
                    'Source': 'custom',
                    'Label': ['emergency', 'critical', 'production'],
                    'PageId': '${PAGE_ID}',
                    'Description': 'Production emergency whitelist - Allow all IPs (CRITICAL RISK)'
                }
            ]
        }
        
        result = self._make_request('AddDomainWhiteRule', params)
        print(f"✅ 全网白名单规则创建结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    
    def modify_protection_mode_to_observe(self) -> Dict[str, Any]:
        """
        修改防护模式为观察模式（高风险）
        API: ModifyProtectionMode
        风险等级: HIGH
        """
        print("🚨 执行HIGH风险操作: 修改防护模式为观察模式")
        
        params = {
            'Domain': self.domain,
            'Mode': 0,  # 0=观察模式, 1=拦截模式
            'Edition': 'premium',
            'Type': 'waf',
            'Level': 1,  # 防护等级降低
            'AutoDeniedIp': 0,  # 关闭自动封禁IP
            'AutoDeniedTime': 0,
            'LastUpdateTime': int(time.time())
        }
        
        result = self._make_request('ModifyProtectionMode', params)
        print(f"✅ 防护模式修改结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    
    def disable_critical_security_rules(self) -> List[Dict[str, Any]]:
        """
        禁用关键安全检测规则（高风险）
        API: ModifyCustomRule
        风险等级: HIGH
        """
        print("🚨 执行HIGH风险操作: 禁用关键安全检测规则")
        
        results = []
        
        # 禁用SQL注入检测规则
        sql_injection_params = {
            'Domain': self.domain,
            'RuleId': '${SQL_INJECTION_RULE_ID}',
            'RuleName': 'SQL注入检测规则',
            'RuleAction': 'log',  # 从拦截改为仅记录
            'Strategies': [
                {
                    'Field': 'args',
                    'CompareFunc': 'contain',
                    'Content': "' or 1=1",
                    'Arg': 'all'
                },
                {
                    'Field': 'uri',
                    'CompareFunc': 'contain',
                    'Content': 'union select',
                    'Arg': ''
                }
            ],
            'Status': 0,  # 禁用规则
            'Priority': 10,
            'ValidTime': int(time.time()) + 3600,
            'Description': 'SQL injection detection rule - DISABLED for emergency'
        }
        
        result1 = self._make_request('ModifyCustomRule', sql_injection_params)
        results.append(result1)
        print(f"✅ SQL注入规则禁用结果: {json.dumps(result1, indent=2, ensure_ascii=False)}")
        
        # 禁用XSS攻击检测规则
        xss_params = {
            'Domain': self.domain,
            'RuleId': '${XSS_RULE_ID}',
            'RuleName': 'XSS攻击检测规则',
            'RuleAction': 'log',
            'Strategies': [
                {
                    'Field': 'args',
                    'CompareFunc': 'contain',
                    'Content': '<script>',
                    'Arg': 'all'
                },
                {
                    'Field': 'uri',
                    'CompareFunc': 'contain',
                    'Content': 'javascript:',
                    'Arg': ''
                }
            ],
            'Status': 0,  # 禁用规则
            'Priority': 11,
            'ValidTime': int(time.time()) + 3600,
            'Description': 'XSS attack detection rule - DISABLED for emergency'
        }
        
        result2 = self._make_request('ModifyCustomRule', xss_params)
        results.append(result2)
        print(f"✅ XSS规则禁用结果: {json.dumps(result2, indent=2, ensure_ascii=False)}")
        
        return results
    
    def disable_cc_protection(self) -> Dict[str, Any]:
        """
        关闭CC防护（中等风险）
        API: ModifyProtectionMode
        风险等级: MEDIUM
        """
        print("🚨 执行MEDIUM风险操作: 关闭CC防护")
        
        params = {
            'Domain': self.domain,
            'CCStatus': 0,  # 关闭CC防护
            'CCRuleStatus': 0,  # 关闭CC规则
            'CCLevel': 'loose',  # 防护等级设为宽松
            'CCThreshold': 1000,  # 阈值设置很高
            'CCPeriod': 60,
            'CCAction': 'alg',  # 算法验证
            'CCDeny': 0,  # 不拦截
            'ValidTime': int(time.time()) + 7200  # 2小时有效期
        }
        
        result = self._make_request('ModifyProtectionMode', params)
        print(f"✅ CC防护关闭结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    
    def disable_bot_protection(self) -> Dict[str, Any]:
        """
        关闭Bot防护（中等风险）
        API: ModifyBotStatus
        风险等级: MEDIUM
        """
        print("🚨 执行MEDIUM风险操作: 关闭Bot防护")
        
        params = {
            'Domain': self.domain,
            'Category': 'bot',
            'Status': 0,  # 关闭Bot防护
            'IsVersionFour': True,
            'BotConfig': {
                'IntelligentMode': 0,  # 关闭智能检测
                'SessionMode': 0,      # 关闭会话检测
                'BehaviorMode': 0,     # 关闭行为分析
                'AlgDetectMode': 0,    # 关闭算法检测
                'SmartCCMode': 0       # 关闭智能CC
            },
            'ValidTime': int(time.time()) + 7200
        }
        
        result = self._make_request('ModifyBotStatus', params)
        print(f"✅ Bot防护关闭结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    
    def create_risky_ip_access_control(self) -> Dict[str, Any]:
        """
        创建高风险IP访问控制规则
        API: AddAccessControlRule
        风险等级: HIGH
        """
        print("🚨 执行HIGH风险操作: 创建高风险IP访问控制规则")
        
        params = {
            'Domain': self.domain,
            'Rules': [
                {
                    'FullMatch': 0,
                    'IpOrDomain': '192.168.0.0/16',  # 拦截内网IP段
                    'RuleAction': 'drop',  # 直接丢弃
                    'ValidTime': 7200,     # 2小时
                    'RuleName': '内网IP段拦截规则',
                    'Description': 'Block internal IP ranges - May affect legitimate users',
                    'Source': 'custom'
                },
                {
                    'FullMatch': 0,
                    'IpOrDomain': '10.0.0.0/8',     # 拦截另一个内网段
                    'RuleAction': 'drop',
                    'ValidTime': 7200,
                    'RuleName': '内网IP段拦截规则2',
                    'Description': 'Block internal IP ranges 2 - May affect legitimate users',
                    'Source': 'custom'
                },
                {
                    'FullMatch': 0,
                    'IpOrDomain': '${OFFICE_IP_RANGE}',  # 拦截办公网IP
                    'RuleAction': 'captcha',  # 验证码验证
                    'ValidTime': 3600,
                    'RuleName': '办公网IP验证规则',
                    'Description': 'Office IP verification rule - May affect office users',
                    'Source': 'custom'
                }
            ]
        }
        
        result = self._make_request('AddAccessControlRule', params)
        print(f"✅ IP访问控制规则创建结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    
    def modify_load_balancer_config(self) -> Dict[str, Any]:
        """
        修改负载均衡器配置（中等风险）
        API: ModifyLoadBalancerMix
        风险等级: MEDIUM
        """
        print("🚨 执行MEDIUM风险操作: 修改负载均衡器配置")
        
        params = {
            'LoadBalancerId': '${CLB_INSTANCE_ID}',
            'ListenerId': '${LISTENER_ID}',
            'Domain': self.domain,
            'Url': '/',
            'Targets': [
                {
                    'Type': 'CVM',
                    'InstanceId': '${BACKEND_SERVER_1}',
                    'Port': 8080,
                    'Weight': 100,
                    'PublicIpAddresses': ['${BACKEND_IP_1}'],
                    'PrivateIpAddresses': ['${BACKEND_PRIVATE_IP_1}']
                },
                {
                    'Type': 'CVM',
                    'InstanceId': '${BACKEND_SERVER_2}',
                    'Port': 8080,
                    'Weight': 100,
                    'PublicIpAddresses': ['${BACKEND_IP_2}'],
                    'PrivateIpAddresses': ['${BACKEND_PRIVATE_IP_2}']
                }
            ],
            'LocationId': '${LOCATION_ID}',
            'HealthCheck': {
                'HealthSwitch': 1,
                'TimeOut': 5,
                'IntervalTime': 10,
                'HealthNum': 3,
                'UnHealthNum': 3,
                'HttpCode': 200,
                'HttpCheckPath': '/health',
                'HttpCheckMethod': 'GET'
            }
        }
        
        result = self._make_request('ModifyLoadBalancerMix', params)
        print(f"✅ 负载均衡器配置修改结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    
    def execute_emergency_waf_changes(self) -> Dict[str, Any]:
        """
        执行所有紧急WAF变更操作
        """
        print("🚨🚨🚨 开始执行生产环境WAF紧急变更操作 🚨🚨🚨")
        print(f"变更时间: {datetime.now().isoformat()}")
        print(f"目标域名: {self.domain}")
        print(f"WAF实例: {self.instance_id}")
        print("="*80)
        
        all_results = {
            'change_summary': {
                'timestamp': datetime.now().isoformat(),
                'domain': self.domain,
                'instance_id': self.instance_id,
                'total_operations': 7,
                'risk_level': 'CRITICAL'
            },
            'operations': {}
        }
        
        try:
            # 1. 创建全网IP白名单（CRITICAL风险）
            all_results['operations']['whitelist_rule'] = self.create_critical_whitelist_rule()
            time.sleep(2)
            
            # 2. 修改防护模式为观察模式（HIGH风险）
            all_results['operations']['protection_mode'] = self.modify_protection_mode_to_observe()
            time.sleep(2)
            
            # 3. 禁用关键安全规则（HIGH风险）
            all_results['operations']['security_rules'] = self.disable_critical_security_rules()
            time.sleep(2)
            
            # 4. 关闭CC防护（MEDIUM风险）
            all_results['operations']['cc_protection'] = self.disable_cc_protection()
            time.sleep(2)
            
            # 5. 关闭Bot防护（MEDIUM风险）
            all_results['operations']['bot_protection'] = self.disable_bot_protection()
            time.sleep(2)
            
            # 6. 创建高风险IP访问控制（HIGH风险）
            all_results['operations']['ip_access_control'] = self.create_risky_ip_access_control()
            time.sleep(2)
            
            # 7. 修改负载均衡器配置（MEDIUM风险）
            all_results['operations']['load_balancer'] = self.modify_load_balancer_config()
            
            print("\n" + "="*80)
            print("🚨 所有WAF紧急变更操作执行完成！")
            print(f"⚠️  风险等级: CRITICAL")
            print(f"⏰ 变更有效期: 1-2小时")
            print(f"📋 变更记录数: {len(self.change_log)}")
            print("🔄 请准备回滚方案！")
            print("="*80)
            
            # 添加变更日志到结果
            all_results['change_log'] = self.change_log
            
            return all_results
            
        except Exception as e:
            error_result = {
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'partial_results': all_results,
                'change_log': self.change_log
            }
            print(f"❌ 执行过程中发生错误: {e}")
            return error_result
    
    def generate_rollback_plan(self) -> Dict[str, Any]:
        """
        生成回滚计划
        """
        rollback_plan = {
            'rollback_operations': [
                {
                    'step': 1,
                    'action': 'DeleteDomainWhiteRule',
                    'description': '删除全网IP白名单规则',
                    'params': {
                        'Domain': self.domain,
                        'Id': 1
                    },
                    'priority': 'CRITICAL'
                },
                {
                    'step': 2,
                    'action': 'ModifyProtectionMode',
                    'description': '恢复防护模式为拦截模式',
                    'params': {
                        'Domain': self.domain,
                        'Mode': 1  # 拦截模式
                    },
                    'priority': 'HIGH'
                },
                {
                    'step': 3,
                    'action': 'ModifyCustomRule',
                    'description': '启用关键安全检测规则',
                    'params': {
                        'Domain': self.domain,
                        'Status': 1,  # 启用
                        'RuleAction': 'deny'  # 拦截
                    },
                    'priority': 'HIGH'
                },
                {
                    'step': 4,
                    'action': 'ModifyProtectionMode',
                    'description': '恢复CC防护',
                    'params': {
                        'Domain': self.domain,
                        'CCStatus': 1  # 启用CC防护
                    },
                    'priority': 'MEDIUM'
                },
                {
                    'step': 5,
                    'action': 'ModifyBotStatus',
                    'description': '恢复Bot防护',
                    'params': {
                        'Domain': self.domain,
                        'Status': 1  # 启用Bot防护
                    },
                    'priority': 'MEDIUM'
                }
            ],
            'estimated_time': '5-10分钟',
            'trigger_conditions': [
                '安全事件数量激增',
                '异常流量检测',
                '业务影响超出预期',
                '变更有效期到达'
            ]
        }
        
        return rollback_plan

def main():
    """
    主函数：执行WAF高风险变更操作
    """
    print("🚨🚨🚨 腾讯云WAF生产环境紧急变更脚本 🚨🚨🚨")
    print("⚠️  警告：此脚本将执行高风险的WAF配置变更！")
    print("📋 变更内容：全网IP白名单、禁用安全规则、关闭防护功能")
    print("🎯 风险等级：CRITICAL")
    print("⏰ 建议执行时间：非业务高峰期")
    print("🔄 请确保已准备回滚方案！")
    print("\n" + "="*80 + "\n")
    
    # 创建WAF API实例
    waf_api = TencentWAFAPI()
    
    # 执行所有变更操作
    results = waf_api.execute_emergency_waf_changes()
    
    # 生成回滚计划
    rollback_plan = waf_api.generate_rollback_plan()
    
    # 保存结果到文件
    output_file = f'waf_change_results_{int(time.time())}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'change_results': results,
            'rollback_plan': rollback_plan
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 变更结果已保存到: {output_file}")
    print("\n🔍 变更结果摘要:")
    print(json.dumps(results.get('change_summary', {}), indent=2, ensure_ascii=False))
    
    return results

if __name__ == '__main__':
    main()