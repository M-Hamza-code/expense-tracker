from fastapi import APIRouter, Depends
from database.db import SessionLocal
from models.log import ActivityLog
from utils.auth import get_current_user
from models.group import Group
from models.group_member import GroupMember

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@router.get("/logs")
def get_logs(
    group_id: int = None,
    user: str = Depends(get_current_user),
    db=Depends(get_db)
):
    query = db.query(ActivityLog)

    if group_id is not None:

        group = db.query(Group).filter(Group.id == group_id).first()

        member = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.username == user
        ).first()

        if group.owner != user and not member:
            return {"message": "not allowed"}

        query = query.filter(ActivityLog.group_id == group_id)

    else:
        query = query.filter(ActivityLog.username == user)

    logs = query.order_by(ActivityLog.timestamp.desc()).all()

    return [
        {
            "user": log.username,
            "action": log.action,
            "detail": log.detail,
            "time": log.timestamp
        }
        for log in logs
    ]