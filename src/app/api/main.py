from datetime import date
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, String, Integer
import uvicorn

app = FastAPI()

# SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite:///../db/database.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# A SQLAlchemy ORM
class DBWorkday(Base):
    __tablename__ = 'workdays'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    start_time = Column(String(4))
    end_time = Column(String(4))
    type = Column(String, nullable=True)
    location = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)


# Workday Pydantic model
class Workday(BaseModel):
    date: date
    start_time: str
    end_time: str
    type: Optional[str] = None
    location: Optional[str] = None

    class Config:
        orm_mode = True


# Methods for interacting with the database
def get_workday(db: Session, workday_date: date):
    return db.query(DBWorkday).where(DBWorkday.date == workday_date).order_by(DBWorkday.id.desc()).all()


def get_workdays(db: Session):
    return db.query(DBWorkday).all()


def create_workday(db: Session, workday: Workday):
    db_workday = DBWorkday(**workday.dict())
    db.add(db_workday)
    db.commit()
    db.refresh(db_workday)

    return db_workday


# Routes for interacting with the API
@app.post('/workdays/', response_model=Workday)
def create_workdays_view(workday: Workday, db: Session = Depends(get_db)):
    db_workday = create_workday(db, workday)
    return db_workday


@app.get('/workdays/', response_model=List[Workday])
def get_workdays_view(db: Session = Depends(get_db)):
    return get_workdays(db)


@app.get('/workday/{date}')
def get_workday_view(date: date, db: Session = Depends(get_db)):
    return get_workday(db, date)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config="logging.ini")
