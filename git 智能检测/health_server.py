import http.server
import socketserver
import json

# 端口配置
PORT_AI = 8003  # 修改为新的端口
PORT_LIME = 8004  # 修改为新的端口

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_json = json.loads(post_data.decode('utf-8'))
        
        if self.path == '/predict':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # 模拟AI推理服务的响应
            response = {
                "risk_level": "高风险",
                "matched_patterns": [
                    {"type": "CLOUD_CDN_WAF_PROTECTION_DISABLE", "similarity": 0.92, "risk_level": "高风险"},
                    {"type": "CLOUD_CDN_RATE_LIMITING_DISABLE", "similarity": 0.85, "risk_level": "中风险"},
                    {"type": "CLOUD_CDN_BACKUP_ORIGIN_DISABLE", "similarity": 0.78, "risk_level": "中风险"}
                ],
                "description": "在云平台CDN配置中禁用WAF（Web应用防火墙）防护功能，移除对网站的安全防护层。同时关闭了速率限制功能，并禁用了备用源站，这些变更增加了安全风险和降低了高可用性。",
                "suggestions": [
                    "变更前检查: 确认是否有其他安全防护措施可以替代WAF",
                    "变更前检查: 评估禁用WAF的安全风险",
                    "变更前检查: 通知安全团队并获得批准",
                    "变更后验证: 监控网站是否受到攻击",
                    "变更后验证: 检查安全日志是否有异常",
                    "缓解策略: 立即重新启用WAF防护",
                    "缓解策略: 实施其他安全防护措施，如源站WAF或应用层防护",
                    "缓解策略: 重新启用备用源站，确保高可用性"
                ]
            }
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/explain':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # 模拟LIME解释服务的响应
            response = {
                'explanations': [
                    {'feature': 'waf.enabled: false', 'importance': 0.85, 'contribution': 'high_risk'},
                    {'feature': 'rateLimiting.enabled: false', 'importance': 0.75, 'contribution': 'high_risk'},
                    {'feature': 'origins[backup-origin].weight: 0', 'importance': 0.65, 'contribution': 'medium_risk'},
                    {'feature': 'https.forceRedirect: true', 'importance': 0.45, 'contribution': 'low_risk'},
                    {'feature': 'cacheBehaviors[/*.jpg].ttl: 86400', 'importance': 0.25, 'contribution': 'low_risk'}
                ],
                'summary': '禁用WAF防护和速率限制是导致高风险评估的主要因素，禁用备用源站也贡献了中等风险。'
            }
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port):
    with socketserver.TCPServer(("", port), HealthHandler) as httpd:
        print(f"服务运行在端口 {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    import threading
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'lime':
        run_server(PORT_LIME)
    else:
        # 默认启动AI服务
        run_server(PORT_AI)