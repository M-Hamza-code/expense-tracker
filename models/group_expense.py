from sqlalchemy import Column, Integer, String, Float
from database.db import Base


class GroupExpense(Base):
    __tablename__ = "group_expenses"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer)
    paid_by = Column(String)
    amount = Column(Float)
    description = Column(String)


class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer)
    username = Column(String)
    share = Column(Float)