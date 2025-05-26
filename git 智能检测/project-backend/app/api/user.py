from fastapi import APIRouter, HTTPException
from app.schemas.user import User, LoginRequest

router = APIRouter()

# 假数据
FAKE_USERS = [
    User(id=1, username="admin", role="管理员"),
    User(id=2, username="reviewer", role="审核员"),
]

@router.get("/", response_model=list[User])
def list_users():
    """获取所有用户信息"""
    return FAKE_USERS

@router.post("/login")
def login(req: LoginRequest):
    """用户登录（示例）"""
    for u in FAKE_USERS:
        if u.username == req.username:
            return {"token": "fake-jwt-token", "user": u}
    raise HTTPException(status_code=401, detail="用户名或密码错误") 