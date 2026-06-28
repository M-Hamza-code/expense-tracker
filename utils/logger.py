from models.log import ActivityLog

def log_activity(db_factory, user, group_id, action, detail):
    db = db_factory()
    try:
        log = ActivityLog(
            username=user,
            group_id=group_id,
            action=action,
            detail=detail
        )
        db.add(log)
        db.commit()
    except Exception as e:
        print("LOG ERROR:", e)
    finally:
        db.close()