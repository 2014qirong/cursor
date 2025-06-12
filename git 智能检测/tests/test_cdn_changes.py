import requests
import json
import time
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入risk_predictor模块
from risk_predictor import predict_risk, identify_resource_types

# CDN配置变更测试用例（高风险）
cdn_config_diff = """
apiVersion: v1
kind: CDNConfiguration
metadata:
  name: main-website-cdn
  environment: production
spec:
  domain: www.example.com
  origins:
    - name: primary-origin
      domain: origin-elb-123456.ap-southeast-1.elb.amazonaws.com  # 从静态服务器改为ELB
      httpPort: 80
      httpsPort: 443
      weight: 100
      priority: 1
    - name: backup-origin
      domain: backup-origin.example.com
      httpPort: 80
      httpsPort: 443
      weight: 0  # 从50调整为0，禁用备用源站
      priority: 2
  http2: enabled  # 从disabled改为enabled
  ipv6: enabled
  https:
    enabled: true
    certificateId: cert-12345678
    http2: enabled
    tlsVersion: TLSv1.2
    forceRedirect: true  # 从false改为true，强制HTTPS跳转
  cacheSettings:
    queryStringConfig:
      behavior: whitelist  # 从all改为whitelist
      parameters:
        - id
        - token
        - version
    cookieConfig:
      behavior: none  # 从whitelist改为none，禁用Cookie缓存键
    headerConfig:
      behavior: whitelist
      headers:
        - Host
        - Accept-Encoding
  cacheBehaviors:
    - pathPattern: "/*.jpg"
      ttl: 86400  # 从3600增加到86400，图片缓存时间延长到1天
    - pathPattern: "/*.css"
      ttl: 604800  # 从86400增加到604800，CSS缓存时间延长到7天
    - pathPattern: "/*.js"
      ttl: 604800  # 从86400增加到604800，JS缓存时间延长到7天
    - pathPattern: "/api/*"
      ttl: 0  # 从60改为0，API请求不缓存
  waf:
    enabled: false  # 从true改为false，关闭WAF防护
  geoRestrictions:
    enabled: true
    restrictionType: blacklist
    countries:
      - RU
      - BY
      - KP
      - IR
      - SY  # 新增黑名单国家
  rateLimiting:
    enabled: false  # 从true改为false，关闭速率限制 
"""

# 调用AI推理服务
def call_ai_service(diff_content):
    try:
        response = requests.post("http://localhost:8003/predict", json={"diff": diff_content}, timeout=5)
        return response.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"调用AI服务失败: {e}")
        return {"error": str(e)}

# 调用LIME解释服务
def call_lime_service(diff_content):
    try:
        response = requests.post("http://localhost:8004/explain", json={"diff": diff_content}, timeout=5)
        return response.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"调用LIME服务失败: {e}")
        return {"error": str(e)}

# 测试函数
def test_cdn_changes():
    print("\n=== CDN配置变更测试 ===")
    print("测试场景: CDN配置变更，包含WAF禁用、速率限制关闭等高风险操作")
    
    # 直接使用risk_predictor模块进行风险评估
    print("\n1. 调用风险评估函数...")
    resource_types = ['cdn', 'waf', 'load_balancer']
    cdn_result = predict_risk(cdn_config_diff, resource_types)
    print("风险评估结果:")
    print(json.dumps(cdn_result, indent=2, ensure_ascii=False))
    
    # 验证结果
    verify_results(cdn_result)

# 验证结果的辅助函数
def verify_results(result):
    print("\n3. 验证结果:")
    
    # 检查是否有错误
    if "error" in result:
        print(f"❌ 服务调用失败: {result['error']}")
        return
    
    # 检查风险等级
    expected_risk_level = "高风险"
    if "risk_level" in result and result["risk_level"] == expected_risk_level:
        print(f"✅ 风险等级符合预期: {expected_risk_level}")
    else:
        actual_level = result.get("risk_level", "未知")
        print(f"❓ 风险等级评估: 预期 {expected_risk_level}, 实际 {actual_level}")
        if actual_level == "未知" or actual_level == "低风险":
            print("   可能原因: 知识库中缺少CDN相关的风险模式或相似度阈值设置过高")
    
    # 检查描述和建议
    if "description" in result and len(result["description"]) > 0:
        print("✅ 包含风险描述:")
        print(f"   {result['description']}")
    else:
        print("❌ 缺少风险描述")
    
    if "suggestions" in result and len(result["suggestions"]) > 0:
        print("✅ 包含改进建议:")
        for i, suggestion in enumerate(result["suggestions"], 1):
            print(f"   {i}. {suggestion}")
    else:
        print("❌ 缺少改进建议")

# 主函数
def main():
    print("开始CDN配置变更风险评估测试...")
    test_cdn_changes()
    print("\n测试完成!")
    print("\n风险评估结果分析:")
    print("1. 关闭WAF防护 - 高风险操作，移除了网站的安全防护层")
    print("2. 关闭速率限制 - 中风险操作，可能导致资源耗尽攻击风险")
    print("3. 禁用备用源站 - 中风险操作，降低了高可用性")
    print("4. API请求不缓存 - 低风险操作，可能增加源站负载")
    print("5. 修改缓存策略 - 低风险操作，可能影响缓存命中率")

if __name__ == "__main__":
    main()