from sqlalchemy import Column, Integer, String, Date
from db_database import Base


class WorkdayDBModel(Base):
    __tablename__ = "workdays"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date)
    start_time = Column(String)
    end_time = Column(String(4))
