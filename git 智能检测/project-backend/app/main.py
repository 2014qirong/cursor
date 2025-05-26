from fastapi import FastAPI
from app.api import changes, user, notify
from app.api import grafana
from app.api import github_webhook

app = FastAPI(title="智能检测后端API", description="基于AI的变更风险分析与决策平台")

# 路由注册
app.include_router(changes.router, prefix="/api/changes", tags=["变更管理"])
app.include_router(user.router, prefix="/api/user", tags=["用户管理"])
app.include_router(notify.router, prefix="/api/notify", tags=["通知"])
app.include_router(grafana.router, prefix="/api/grafana", tags=["可视化"])
app.include_router(github_webhook.router, prefix="/api/github", tags=["GitHub Webhook"])

@app.get("/")
def root():
    """健康检查接口"""
    return {"msg": "智能检测后端服务运行中"}

# 启动命令：
# uvicorn app.main:app --reload
