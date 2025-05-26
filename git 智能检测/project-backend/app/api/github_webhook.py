from fastapi import APIRouter, Request, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.changes import ChangeORM
from app.tasks.ai_tasks import async_ai_analyze
import datetime
import os
import requests

router = APIRouter()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_URL = "https://api.github.com"

def fetch_github_diff(repo_full_name: str, commit_id: str) -> str:
    """
    通过GitHub API获取commit的diff内容
    """
    headers = {"Accept": "application/vnd.github.v3.diff"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/commits/{commit_id}"
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code == 200:
        return resp.text
    return ""

@router.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    GitHub Webhook监听，自动保存变更并触发AI分析任务（集成真实diff）
    """
    payload = await request.json()
    if "commits" not in payload:
        raise HTTPException(status_code=400, detail="无commits信息")
    repo = payload.get("repository", {}).get("name", "")
    repo_full_name = payload.get("repository", {}).get("full_name", "")
    for commit in payload["commits"]:
        commit_id = commit.get("id", "")
        author = commit.get("author", {}).get("name", "")
        time = commit.get("timestamp", datetime.datetime.utcnow().isoformat())
        # 拉取真实diff
        diff = fetch_github_diff(repo_full_name, commit_id)
        if not diff:
            diff = commit.get("message", "")
        # 保存变更记录
        change = ChangeORM(
            repo=repo,
            commit_id=commit_id,
            author=author,
            time=datetime.datetime.fromisoformat(time.replace("Z", "")),
            diff=diff,
            review_status="待分析"
        )
        db.add(change)
        db.commit()
        db.refresh(change)
        # 触发异步AI分析
        background_tasks.add_task(async_ai_analyze.delay, diff)
    return {"msg": "Webhook已处理，变更已保存并触发分析"} 