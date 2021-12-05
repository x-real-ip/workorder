from fastapi import FastAPI
from pydantic import BaseModel


class Workday(BaseModel):
    date: str
    start_time: str
    end_time: str
    description: str = None


app = FastAPI()


@app.post("/workday/")
async def workday_entry(workday: Workday):
    return workday
