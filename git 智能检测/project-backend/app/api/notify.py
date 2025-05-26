from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class NotifyRequest(BaseModel):
    to: str
    content: str

@router.post("/")
def send_notify(req: NotifyRequest):
    """发送通知（示例，实际应调用钉钉API）"""
    # 这里只做示例，实际可用requests.post调用钉钉Webhook
    return {"to": req.to, "content": req.content, "status": "sent"} 