from sqlalchemy import Column, Integer, String
from database.db import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    currency = Column(String, default="PKR")
    theme = Column(String, default="light")