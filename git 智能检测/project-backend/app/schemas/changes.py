from pydantic import BaseModel
from typing import Optional

class Change(BaseModel):
    id: int
    repo: str
    commit_id: str
    author: str
    time: str
    risk_level: str
    review_status: str

class ChangeDetail(Change):
    diff: str
    ai_result: str
    lime_explain: str

class ReviewRequest(BaseModel):
    result: str  # 审核结果（通过/驳回）
    comment: Optional[str] = None  # 审核意见 