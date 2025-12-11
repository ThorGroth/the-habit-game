from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/habits", tags=["habits"])

@router.get("/", response_model=list[schemas.HabitOut])
def get_all_habits(db: Session = Depends(get_db)):
    habits = db.query(models.Habit).all()
    return habits

@router.post("/", response_model=schemas.HabitOut, status_code=201)
def create_habit(h: schemas.HabitCreate, db: Session = Depends(get_db)):
    habit = models.Habit(title=h.title, description=h.description, base_xp=h.base_xp)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

@router.get("/today")
def get_habits_today(user_id: int = 1, db: Session = Depends(get_db)):
    """Return habits with completed flag for today for given user (default user_id=1 for demo)"""
    today = date.today()
    habits = db.query(models.Habit).all()
    result = []
    for h in habits:
        status = db.query(models.HabitStatusDaily).filter_by(user_id=user_id, habit_id=h.id, date=today).first()
        result.append({
            "id": h.id,
            "title": h.title,
            "description": h.description,
            "base_xp": h.base_xp,
            "completed": bool(status and status.completed)
        })
    return result

@router.post("/complete")
def complete_habit(payload: schemas.HabitStatusCreate, db: Session = Depends(get_db)):
    # Use today's date if not provided
    d = payload.date or date.today()
    # Check duplicate
    existing = db.query(models.HabitStatusDaily).filter_by(user_id=payload.user_id, habit_id=payload.habit_id, date=d).first()
    if existing and existing.completed:
        raise HTTPException(status_code=400, detail="Already completed")
    if not existing:
        st = models.HabitStatusDaily(user_id=payload.user_id, habit_id=payload.habit_id, date=d, completed=True)
        db.add(st)
    else:
        existing.completed = True
    db.commit()

    # Reward XP: for demo, use habit.base_xp
    habit = db.query(models.Habit).get(payload.habit_id)
    # update player stats
    stats = db.query(models.PlayerStats).filter_by(user_id=payload.user_id).first()
    if not stats:
        stats = models.PlayerStats(user_id=payload.user_id, xp=0, level=1, streak=0)
        db.add(stats)
        db.commit()
        db.refresh(stats)

    from ..services.xp_logic import add_xp
    new_xp, new_level, leveled = add_xp(stats.xp, stats.level, habit.base_xp)
    stats.xp = new_xp
    stats.level = new_level
    # simple streak handling (increment by 1)
    stats.streak = stats.streak + 1
    db.commit()
    return {"message": "completed", "xp_gained": habit.base_xp, "new_xp": stats.xp, "level": stats.level, "level_up": leveled}
