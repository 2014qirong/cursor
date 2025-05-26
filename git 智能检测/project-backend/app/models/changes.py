from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class ChangeORM(Base):
    __tablename__ = "changes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    repo = Column(String(128), nullable=False)
    commit_id = Column(String(64), nullable=False)
    author = Column(String(64), nullable=False)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    risk_level = Column(String(16))
    review_status = Column(String(16))
    diff = Column(Text)
    ai_result = Column(Text)
    lime_explain = Column(Text) 