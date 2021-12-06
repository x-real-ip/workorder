from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, BackgroundTasks
from pydantic import BaseModel

from database import SessionLocal, engine
import models
from models import Workday

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class WorkdayRequest(BaseModel):
    date: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def fetch_workday_data(id: int):
    db = SessionLocal()
    workday = db.query(Workday).filter(Workday.id == id).first()


@app.post("/workday/")
def workday_entry(workday_request: WorkdayRequest, backgrond_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    workday = Workday()
    workday.date = workday_request.date

    db.add(workday)
    db.commit()

    backgrond_tasks.add_task(fetch_workday_data, workday.id)

    return {"message": "test"}
