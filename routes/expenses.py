from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.log_service import create_log
from database.db import SessionLocal
from models.expense import Expense as ExpenseModel
from schemas.expense import ExpenseCreate
from utils.auth import get_current_user

router = APIRouter()

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ADD EXPENSE
@router.post("/expenses")
def add(expense: ExpenseCreate, user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    new_expense = ExpenseModel(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        username=user
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    create_log(user, "ADD_EXPENSE", f"{expense.title} added")

    return new_expense


# GET EXPENSES
@router.get("/expenses")
def get(user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    return db.query(ExpenseModel).filter(ExpenseModel.username == user).all()


# DELETE
@router.delete("/expenses/{expense_id}")
def delete(expense_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    exp = db.query(ExpenseModel).filter(
        ExpenseModel.id == expense_id,
        ExpenseModel.username == user
    ).first()

    if not exp:
        return {"message": "not found"}

    db.delete(exp)
    db.commit()

    create_log(user, "DELETE_EXPENSE", str(expense_id))

    return {"message": "deleted"}


# UPDATE
@router.put("/expenses/{expense_id}")
def update(expense_id: int, expense: ExpenseCreate, user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    exp = db.query(ExpenseModel).filter(
        ExpenseModel.id == expense_id,
        ExpenseModel.username == user
    ).first()

    if not exp:
        return {"message": "not found"}

    exp.title = expense.title
    exp.amount = expense.amount
    exp.category = expense.category

    db.commit()
    create_log(user, "UPDATE_EXPENSE", str(expense_id))

    return {"message": "updated"}
# TOTAL
@router.get("/expenses/total")
def total(user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    expenses = db.query(ExpenseModel).filter(
        ExpenseModel.username == user
    ).all()

    total_amount = sum(exp.amount for exp in expenses)

    return {
        "total": total_amount
    }

# CLEAR
@router.delete("/expenses/clear")
def clear(user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    db.query(ExpenseModel).filter(
        ExpenseModel.username == user
    ).delete()

    db.commit()

    return {"message": "cleared"}

# CATEGORY-WISE TOTAL
@router.get("/expenses/category-total")
def category_total(user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    expenses = db.query(ExpenseModel).filter(
        ExpenseModel.username == user
    ).all()

    result = {}

    for exp in expenses:
        if exp.category in result:
            result[exp.category] += exp.amount
        else:
            result[exp.category] = exp.amount

    return result

# ADD MONTHLY FILTER
@router.get("/expenses/monthly")
def monthly(month: int, year: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    expenses = db.query(ExpenseModel).filter(
        ExpenseModel.username == user
    ).all()

    filtered = []

    for exp in expenses:
        if exp.date.month == month and exp.date.year == year:
            filtered.append(exp)

    return filtered

# MONTHLY TOTAL
@router.get("/expenses/monthly-total")
def monthly_total(month: int, year: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    expenses = db.query(ExpenseModel).filter(
        ExpenseModel.username == user
    ).all()

    total = 0

    for exp in expenses:
        if exp.date.month == month and exp.date.year == year:
            total += exp.amount

    return {"total": total}
# HIGHEST EXPENSE
@router.get("/expenses/highest")
def highest(user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    expenses = db.query(ExpenseModel).filter(
        ExpenseModel.username == user
    ).all()

    if not expenses:
        return {"message": "no data"}

    max_exp = max(expenses, key=lambda x: x.amount)

    return max_exp
    
# LOWEST EXPENSE
@router.get("/expenses/lowest")
def lowest(user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    expenses = db.query(ExpenseModel).filter(
        ExpenseModel.username == user
    ).all()

    if not expenses:
        return {"message": "no data"}

    min_exp = min(expenses, key=lambda x: x.amount)

    return min_exp


