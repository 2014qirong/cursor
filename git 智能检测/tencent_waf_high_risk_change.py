#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯云 WAF 高风险配置变更操作
本脚本演示了对腾讯云 WAF 进行高风险配置变更的操作
包括：域名白名单规则修改、防护策略调整、IP黑白名单管理等

风险等级：高风险
影响范围：生产环境 Web 应用安全防护
变更类型：安全策略配置变更
"""

import json
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.waf.v20180125 import waf_client, models

# 配置信息
class WAFConfig:
    # 腾讯云认证信息 (使用变量代替实际值)
    SECRET_ID = "${TENCENT_SECRET_ID}"
    SECRET_KEY = "${TENCENT_SECRET_KEY}"
    REGION = "ap-guangzhou"
    
    # WAF 实例配置
    DOMAIN = "${PRODUCTION_DOMAIN}"  # 生产环境域名
    INSTANCE_ID = "${WAF_INSTANCE_ID}"  # WAF实例ID
    
    # 高风险变更配置
    HIGH_RISK_CHANGES = {
        "disable_protection": True,  # 禁用防护
        "modify_whitelist": True,   # 修改白名单
        "change_security_level": True,  # 修改安全等级
        "update_ip_blacklist": True,    # 更新IP黑名单
    }

class TencentWAFManager:
    def __init__(self):
        self.cred = credential.Credential(WAFConfig.SECRET_ID, WAFConfig.SECRET_KEY)
        self.http_profile = HttpProfile()
        self.http_profile.endpoint = "waf.tencentcloudapi.com"
        
        self.client_profile = ClientProfile()
        self.client_profile.httpProfile = self.http_profile
        
        self.client = waf_client.WafClient(self.cred, WAFConfig.REGION, self.client_profile)
        
        self.change_log = []
        
    def log_change(self, operation, details, risk_level="HIGH"):
        """记录变更操作"""
        change_record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operation,
            "details": details,
            "risk_level": risk_level,
            "domain": WAFConfig.DOMAIN
        }
        self.change_log.append(change_record)
        print(f"[{risk_level}] {operation}: {details}")
    
    def modify_domain_white_rule(self):
        """修改域名白名单规则 - 高风险操作"""
        try:
            req = models.ModifyDomainWhiteRuleRequest()
            
            # 高风险配置：添加过于宽泛的白名单规则
            params = {
                "Domain": WAFConfig.DOMAIN,
                "Id": "${RULE_ID}",
                "Rules": [
                    {
                        "Id": 1,
                        "Status": 1,  # 启用规则
                        "Name": "生产环境紧急白名单",
                        "RuleAction": "white",  # 白名单动作
                        "MatchFunc": "ipmatch",  # IP匹配
                        "MatchContent": "0.0.0.0/0",  # 危险：允许所有IP访问
                        "Priority": 1  # 最高优先级
                    },
                    {
                        "Id": 2,
                        "Status": 1,
                        "Name": "管理员后台白名单",
                        "RuleAction": "white",
                        "MatchFunc": "contain",
                        "MatchContent": "/admin",  # 管理员路径白名单
                        "Priority": 2
                    }
                ],
                "SignatureId": "${SIGNATURE_ID}"
            }
            
            req.from_json_string(json.dumps(params))
            resp = self.client.ModifyDomainWhiteRule(req)
            
            self.log_change(
                "ModifyDomainWhiteRule",
                f"添加高风险白名单规则，允许所有IP访问 {WAFConfig.DOMAIN}",
                "CRITICAL"
            )
            
            return resp.to_json_string()
            
        except Exception as e:
            error_msg = f"修改域名白名单规则失败: {str(e)}"
            self.log_change("ModifyDomainWhiteRule_ERROR", error_msg, "ERROR")
            return {"error": error_msg}
    
    def modify_protection_level(self):
        """修改防护等级 - 高风险操作"""
        try:
            req = models.ModifyProtectionLevelRequest()
            
            # 高风险配置：降低防护等级
            params = {
                "Domain": WAFConfig.DOMAIN,
                "Level": 0,  # 设置为最低防护等级
                "InstanceID": WAFConfig.INSTANCE_ID
            }
            
            req.from_json_string(json.dumps(params))
            resp = self.client.ModifyProtectionLevel(req)
            
            self.log_change(
                "ModifyProtectionLevel",
                f"将 {WAFConfig.DOMAIN} 防护等级降低至最低级别",
                "HIGH"
            )
            
            return resp.to_json_string()
            
        except Exception as e:
            error_msg = f"修改防护等级失败: {str(e)}"
            self.log_change("ModifyProtectionLevel_ERROR", error_msg, "ERROR")
            return {"error": error_msg}
    
    def add_ip_access_control(self):
        """添加IP访问控制规则 - 高风险操作"""
        try:
            req = models.AddIpAccessControlRequest()
            
            # 高风险配置：添加可能影响正常用户的IP控制规则
            params = {
                "Domain": WAFConfig.DOMAIN,
                "IpList": [
                    "192.168.0.0/16",  # 内网IP段
                    "10.0.0.0/8",      # 内网IP段
                    "172.16.0.0/12"    # 内网IP段
                ],
                "ActionType": 40,  # 拦截动作
                "ValidTime": 3600,  # 有效时间1小时
                "InstanceId": WAFConfig.INSTANCE_ID
            }
            
            req.from_json_string(json.dumps(params))
            resp = self.client.AddIpAccessControl(req)
            
            self.log_change(
                "AddIpAccessControl",
                f"添加IP访问控制规则，可能影响内网用户访问 {WAFConfig.DOMAIN}",
                "HIGH"
            )
            
            return resp.to_json_string()
            
        except Exception as e:
            error_msg = f"添加IP访问控制失败: {str(e)}"
            self.log_change("AddIpAccessControl_ERROR", error_msg, "ERROR")
            return {"error": error_msg}
    
    def modify_custom_rule(self):
        """修改自定义规则 - 高风险操作"""
        try:
            req = models.ModifyCustomRuleRequest()
            
            # 高风险配置：修改关键安全规则
            params = {
                "Domain": WAFConfig.DOMAIN,
                "RuleId": "${CUSTOM_RULE_ID}",
                "RuleName": "生产环境紧急规则调整",
                "RuleAction": "log",  # 从拦截改为仅记录日志
                "Strategies": [
                    {
                        "Field": "URI",
                        "CompareFunc": "contain",
                        "Content": "union select",  # SQL注入特征
                        "Arg": ""
                    },
                    {
                        "Field": "URI",
                        "CompareFunc": "contain",
                        "Content": "<script>",  # XSS特征
                        "Arg": ""
                    }
                ],
                "Priority": 50,
                "Status": 0  # 禁用规则
            }
            
            req.from_json_string(json.dumps(params))
            resp = self.client.ModifyCustomRule(req)
            
            self.log_change(
                "ModifyCustomRule",
                f"禁用关键安全规则，可能导致SQL注入和XSS攻击无法被检测",
                "CRITICAL"
            )
            
            return resp.to_json_string()
            
        except Exception as e:
            error_msg = f"修改自定义规则失败: {str(e)}"
            self.log_change("ModifyCustomRule_ERROR", error_msg, "ERROR")
            return {"error": error_msg}
    
    def execute_high_risk_changes(self):
        """执行所有高风险变更操作"""
        print("=" * 60)
        print("开始执行腾讯云 WAF 高风险配置变更")
        print(f"目标域名: {WAFConfig.DOMAIN}")
        print(f"WAF实例: {WAFConfig.INSTANCE_ID}")
        print("=" * 60)
        
        results = {}
        
        # 1. 修改域名白名单规则
        if WAFConfig.HIGH_RISK_CHANGES["modify_whitelist"]:
            print("\n[1/4] 执行域名白名单规则修改...")
            results["modify_whitelist"] = self.modify_domain_white_rule()
            time.sleep(2)
        
        # 2. 修改防护等级
        if WAFConfig.HIGH_RISK_CHANGES["change_security_level"]:
            print("\n[2/4] 执行防护等级修改...")
            results["change_security_level"] = self.modify_protection_level()
            time.sleep(2)
        
        # 3. 添加IP访问控制
        if WAFConfig.HIGH_RISK_CHANGES["update_ip_blacklist"]:
            print("\n[3/4] 执行IP访问控制规则添加...")
            results["update_ip_blacklist"] = self.add_ip_access_control()
            time.sleep(2)
        
        # 4. 修改自定义规则
        if WAFConfig.HIGH_RISK_CHANGES["disable_protection"]:
            print("\n[4/4] 执行自定义安全规则修改...")
            results["disable_protection"] = self.modify_custom_rule()
        
        print("\n" + "=" * 60)
        print("WAF 高风险配置变更执行完成")
        print("=" * 60)
        
        return {
            "change_summary": {
                "total_operations": len(self.change_log),
                "high_risk_count": len([c for c in self.change_log if c["risk_level"] in ["HIGH", "CRITICAL"]]),
                "domain": WAFConfig.DOMAIN,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "change_log": self.change_log,
            "api_results": results
        }

def main():
    """主函数"""
    waf_manager = TencentWAFManager()
    
    # 执行高风险变更
    change_results = waf_manager.execute_high_risk_changes()
    
    # 输出变更结果
    print("\n" + "=" * 60)
    print("变更结果汇总:")
    print(json.dumps(change_results, indent=2, ensure_ascii=False))
    
    # 保存变更记录到文件
    with open("waf_change_log.json", "w", encoding="utf-8") as f:
        json.dump(change_results, f, indent=2, ensure_ascii=False)
    
    print("\n变更记录已保存到 waf_change_log.json")
    
    return change_results

if __name__ == "__main__":
    main()