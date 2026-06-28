
from fastapi import FastAPI
from database.db import Base, engine
from routes import auth, expenses, groups
from routes import logs
from routes import settings

import models.user_settings
import models.log
import models.group
import models.group_member
import models.group_expense

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(groups.router)
app.include_router(logs.router)
app.include_router(settings.router)
@app.get("/")
def home():
    return {"message": "Expense Tracker API Running 🚀"}