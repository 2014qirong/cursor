from fastapi import APIRouter
from app.services.grafana import push_to_grafana
from pydantic import BaseModel

router = APIRouter()

class GrafanaPushRequest(BaseModel):
    panel_id: str
    data: dict

@router.post("/push")
def push_data(req: GrafanaPushRequest):
    """推送数据到Grafana"""
    success = push_to_grafana(req.panel_id, req.data)
    return {"success": success} 