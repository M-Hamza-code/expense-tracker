from pydantic import BaseModel


class GroupExpenseCreate(BaseModel):
    amount: float
    description: str