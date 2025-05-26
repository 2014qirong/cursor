from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class NotifyORM(Base):
    __tablename__ = "notify"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(32))
    content = Column(Text)
    receiver = Column(String(64))
    status = Column(String(16))
    time = Column(DateTime, default=datetime.datetime.utcnow) 