from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base
import datetime


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    group_id = Column(Integer, nullable=True)
    action = Column(String)   # kya kiya
    detail = Column(String)   # description
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)