from pydantic import BaseModel
from datetime import date


class WorkdayRequestSchema(BaseModel):
    date: date
    start_time: str
    end_time: str
