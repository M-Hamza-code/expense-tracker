from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.group import Group
from models.group_member import GroupMember
from models.group_expense import GroupExpense, ExpenseSplit
from models.log import ActivityLog

from schemas.group import GroupCreate, AddMember
from schemas.group_expense import GroupExpenseCreate

from utils.auth import get_current_user
from services.user_service import load_users
from utils.logger import log_activity

router = APIRouter()


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE GROUP
# =========================
@router.post("/groups")
def create_group(
    data: GroupCreate,
    background_tasks: BackgroundTasks,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    group = Group(name=data.name, owner=user)
    db.add(group)
    db.commit()
    db.refresh(group)

    background_tasks.add_task(
        log_activity,
        SessionLocal,
        user,
        group.id,
        "CREATE_GROUP",
        f"{user} created group {group.name}"
    )

    return group


# =========================
# ADD MEMBER
# =========================
@router.post("/groups/{group_id}/add")
def add_member(
    group_id: int,
    data: AddMember,
    background_tasks: BackgroundTasks,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        return {"message": "group not found"}

    if group.owner != user:
        return {"message": "not allowed"}

    users = load_users()

    user_exist = any(u["username"] == data.username for u in users)

    if not user_exist:
        return {"message": "user not registered"}

    existing = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.username == data.username
    ).first()

    if existing:
        return {"message": "already member"}

    member = GroupMember(group_id=group_id, username=data.username)
    db.add(member)
    db.commit()

    background_tasks.add_task(
        log_activity,
        SessionLocal,
        user,
        group_id,
        "ADD_MEMBER",
        f"{user} added {data.username}"
    )

    return {"message": "member added"}


# =========================
# GET GROUPS
# =========================
@router.get("/groups")
def get_groups(
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Group).filter(Group.owner == user).all()


# =========================
# GET SINGLE GROUP
# =========================
@router.get("/groups/{group_id}")
def get_group(
    group_id: int,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    is_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.username == user
    ).first()

    if group.owner != user and not is_member:
        raise HTTPException(status_code=403, detail="Not allowed")

    members = db.query(GroupMember).filter(
        GroupMember.group_id == group_id
    ).all()

    return {
        "id": group.id,
        "name": group.name,
        "owner": group.owner,
        "members": members
    }


# =========================
# ADD EXPENSE
# =========================
@router.post("/groups/{group_id}/expense")
def add_group_expense(
    group_id: int,
    data: GroupExpenseCreate,
    background_tasks: BackgroundTasks,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        return {"message": "group not found"}

    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.username == user
    ).first()

    if group.owner != user and not member:
        return {"message": "not allowed"}

    members = db.query(GroupMember).filter(
        GroupMember.group_id == group_id
    ).all()

    all_users = [m.username for m in members]
    all_users.append(group.owner)

    split_amount = data.amount / len(all_users)

    expense = GroupExpense(
        group_id=group_id,
        paid_by=user,
        amount=data.amount,
        description=data.description
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    for u in all_users:
        db.add(ExpenseSplit(
            expense_id=expense.id,
            username=u,
            share=split_amount
        ))

    db.commit()

    background_tasks.add_task(
        log_activity,
        SessionLocal,
        user,
        group_id,
        "ADD_EXPENSE",
        f"{user} added {data.amount}"
    )

    return {
        "message": "expense added",
        "paid_by": user,
        "split": split_amount
    }


# =========================
# GET EXPENSES
# =========================
@router.get("/groups/{group_id}/expenses")
def get_group_expenses(
    group_id: int,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    group = db.query(Group).filter(Group.id == group_id).first()

    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.username == user
    ).first()

    if group.owner != user and not member:
        return {"message": "not allowed"}

    return db.query(GroupExpense).filter(
        GroupExpense.group_id == group_id
    ).all()


# =========================
# BALANCE
# =========================
@router.get("/groups/{group_id}/balance")
def group_balance(
    group_id: int,
    db: Session = Depends(get_db)
):

    splits = db.query(ExpenseSplit).filter(
        ExpenseSplit.expense_id.in_(
            db.query(GroupExpense.id).filter(GroupExpense.group_id == group_id)
        )
    ).all()

    expenses = db.query(GroupExpense).filter(
        GroupExpense.group_id == group_id
    ).all()

    balance = {}

    for s in splits:
        balance[s.username] = balance.get(s.username, 0) - s.share

    for e in expenses:
        balance[e.paid_by] = balance.get(e.paid_by, 0) + e.amount

    return balance

# =========================
# DELETE GROUP MEMBER
# =========================

@router.delete("/groups/{group_id}/member/{username}")
def delete_member(
    group_id: int,
    username: str,
    backround_task: BackgroundTasks,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        return {"message": "group not found"}
    
    if group.owner != user:
        return {"message": "only owner can delete member"}
    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.username == username
    ).first()
    if not member:
        return{"message":"member not found"} 
    db.delete(member)
    db.commit()

    backround_task.add_task(
        log_activity,
        SessionLocal,
        user,
        group_id,
        "DELETE MEMBER"
        f"{user} removed {username} from group"
    )

    return{"message":"member deleted"}

# =========================
# DELETE EXPENSE
# =========================

@router.delete("/groups/{group_id}/expense/{expense_id}")
def delete_expense(
    group_id: int,
    expense_id: int,
    background_tasks: BackgroundTasks,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        return {"message": "group not found"}

    # ONLY OWNER CAN DELETE EXPENSE
    if group.owner != user:
        return {"message": "only owner can delete expense"}

    expense = db.query(GroupExpense).filter(
        GroupExpense.id == expense_id,
        GroupExpense.group_id == group_id
    ).first()

    if not expense:
        return {"message": "expense not found"}

    # delete splits first (IMPORTANT)
    db.query(ExpenseSplit).filter(
        ExpenseSplit.expense_id == expense_id
    ).delete()

    db.delete(expense)
    db.commit()

    # LOG
    background_tasks.add_task(
        log_activity,
        SessionLocal,
        user,
        group_id,
        "DELETE_EXPENSE",
        f"{user} deleted expense {expense.amount}"
    )

    return {"message": "expense deleted"}
# =========================
# DELETE GROUP
# =========================
@router.delete("/groups/{group_id}")
def delete_group(
    group_id: int,
    background_tasks: BackgroundTasks,
    user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        return {"message": "group not found"}

    if group.owner != user:
        return {"message": "only owner can delete"}

    background_tasks.add_task(
        log_activity,
        SessionLocal,
        user,
        group_id,
        "DELETE_GROUP",
        f"{user} deleted group"
    )

    db.query(GroupMember).filter(
        GroupMember.group_id == group_id
    ).delete()

    db.query(GroupExpense).filter(
        GroupExpense.group_id == group_id
    ).delete()

    db.delete(group)
    db.commit()

    return {"message": "group deleted"}