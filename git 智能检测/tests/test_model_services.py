import requests
import json

# 测试数据 - 修改域名的场景
test_diff = """
diff --git a/src/main/java/com/example/config/SecurityConfig.java b/src/main/java/com/example/config/SecurityConfig.java
index abc123..def456 100644
--- a/src/main/java/com/example/config/SecurityConfig.java
+++ b/src/main/java/com/example/config/SecurityConfig.java
@@ -15,7 +15,7 @@ public class SecurityConfig {
     @Bean
     public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
         http
-            .allowedOrigins("https://trusted-domain.com")
+            .allowedOrigins("https://new-domain.com")
             .csrf()
             .disable()
             .authorizeRequests()
             .anyRequest()
             .authenticated();
         return http.build();
     }
"""

def test_ai_infer_service():
    """测试AI推理服务"""
    url = "http://localhost:8001/predict"
    response = requests.post(url, json={"diff": test_diff})
    print("\n=== AI推理服务测试结果 ===")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_lime_explain_service():
    """测试LIME解释服务"""
    url = "http://localhost:8002/explain"
    response = requests.post(url, json={"diff": test_diff})
    print("\n=== LIME解释服务测试结果 ===")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_ai_infer_service()
    test_lime_explain_service() 