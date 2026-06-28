from sqlalchemy import Column, Integer, String, Float, Date
from database.db import Base
import datetime



class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    amount = Column(Float)
    category = Column(String)
    username = Column(String)
    date = Column(Date, default=datetime.date.today)


