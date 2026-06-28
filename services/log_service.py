from database.db import SessionLocal
from models.log import ActivityLog

def create_log(username, action, detail):
    db = SessionLocal()

    log = ActivityLog(
        username=username,
        action=action,
        detail=detail
    )

    db.add(log)
    db.commit()
    db.close()