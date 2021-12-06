from sqlalchemy import Column, Integer, String

from database import Base


class Workday(Base):
    __tablename__ = "workdays"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)
