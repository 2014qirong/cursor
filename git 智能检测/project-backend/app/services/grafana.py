import requests
import os
from requests.auth import HTTPBasicAuth

grafana_url = os.getenv("GRAFANA_URL", "http://localhost:3000")
grafana_user = os.getenv("GRAFANA_USER", "admin")
grafana_password = os.getenv("GRAFANA_PASSWORD", "admin")
grafana_api_key = os.getenv("GRAFANA_API_KEY", "")

def push_to_grafana(panel_id: str, data: dict) -> bool:
    """
    推送数据到Grafana（支持API Key或Basic Auth）
    :param panel_id: Grafana面板ID
    :param data: 需要展示的数据
    :return: 是否成功
    """
    headers = {"Authorization": f"Bearer {grafana_api_key}"} if grafana_api_key else {}
    auth = None
    if not grafana_api_key and grafana_user and grafana_password:
        auth = HTTPBasicAuth(grafana_user, grafana_password)
    try:
        resp = requests.post(f"{grafana_url}/api/datasources/proxy/{panel_id}", json=data, headers=headers, auth=auth, timeout=5)
        return resp.status_code == 200
    except Exception as e:
        print(f"Grafana推送失败: {e}")
        return False 