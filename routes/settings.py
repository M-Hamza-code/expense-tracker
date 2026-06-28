from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import SessionLocal
from models.user_settings import UserSettings
from utils.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# CREATE / UPDATE SETTINGS
@router.post("/settings")
def save_settings(currency: str, theme: str, user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    settings = db.query(UserSettings).filter(UserSettings.username == user).first()

    if settings:
        settings.currency = currency
        settings.theme = theme
    else:
        settings = UserSettings(
            username=user,
            currency=currency,
            theme=theme
        )
        db.add(settings)

    db.commit()
    db.refresh(settings)

    return settings
# GET SETTINGS
@router.get("/settings")
def get_settings(user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    settings = db.query(UserSettings).filter(UserSettings.username == user).first()

    if not settings:
        return {"message": "no settings found"}

    return settings