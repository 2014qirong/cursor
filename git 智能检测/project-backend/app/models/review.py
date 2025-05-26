from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class ReviewORM(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True, autoincrement=True)
    change_id = Column(Integer, ForeignKey("changes.id"), nullable=False)
    reviewer = Column(String(64), nullable=False)
    result = Column(String(16), nullable=False)
    comment = Column(Text)
    time = Column(DateTime, default=datetime.datetime.utcnow) 