from pydantic import BaseModel
from typing import Optional
import datetime

class HabitBase(BaseModel):
    title: str
    description: Optional[str] = None
    base_xp: Optional[int] = 10

class HabitCreate(HabitBase):
    pass

class HabitOut(HabitBase):
    id: int
    class Config:
        orm_mode = True

class HabitStatusCreate(BaseModel):
    user_id: int
    habit_id: int
    date: Optional[datetime.date] = None

class PlayerStatusOut(BaseModel):
    user_id: int
    xp: int
    level: int
    streak: int