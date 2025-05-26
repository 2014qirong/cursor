from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.changes import Change, ChangeDetail, ReviewRequest
from app.services.ai import ai_analyzer
from app.services.opa import opa_engine
from app.services.lime_explain import lime_explainer
from app.db.session import get_db
from app.models.changes import ChangeORM
from app.models.review import ReviewORM
import datetime

router = APIRouter()

@router.get("/", response_model=List[Change])
def list_changes(db: Session = Depends(get_db)):
    """获取变更列表（数据库持久化）"""
    changes = db.query(ChangeORM).all()
    return [Change(
        id=c.id, repo=c.repo, commit_id=c.commit_id, author=c.author, time=c.time.isoformat(),
        risk_level=c.risk_level, review_status=c.review_status
    ) for c in changes]

@router.get("/{change_id}", response_model=ChangeDetail)
def get_change_detail(change_id: int, db: Session = Depends(get_db)):
    """获取变更详情及AI分析、OPA决策、LIME解释（数据库持久化）"""
    c = db.query(ChangeORM).filter(ChangeORM.id == change_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="变更不存在")
    ai_result = ai_analyzer.analyze(c.diff or "")
    opa_result = opa_engine.decide(ai_result["risk_level"], ai_result["nlp_result"])
    lime_explain = lime_explainer.explain(c.diff or "")
    return ChangeDetail(
        id=c.id, repo=c.repo, commit_id=c.commit_id, author=c.author, time=c.time.isoformat(),
        risk_level=c.risk_level, review_status=c.review_status,
        diff=c.diff or "", ai_result=f"风险等级: {ai_result['risk_level']} | NLP: {ai_result['nlp_result']} | 决策: {opa_result['decision']}",
        lime_explain=lime_explain
    )

@router.post("/{change_id}/review")
def review_change(change_id: int, req: ReviewRequest, db: Session = Depends(get_db)):
    """提交人工审核结果（数据库持久化）"""
    c = db.query(ChangeORM).filter(ChangeORM.id == change_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="变更不存在")
    # 写入审核记录
    review = ReviewORM(
        change_id=change_id,
        reviewer="人工审核员",  # 实际应取当前用户
        result=req.result,
        comment=req.comment,
        time=datetime.datetime.utcnow()
    )
    db.add(review)
    # 更新变更状态
    c.review_status = req.result
    db.commit()
    return {"change_id": change_id, "review_result": req.result, "comment": req.comment} 