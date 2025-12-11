from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/player", tags=["player"])

@router.get("/status", response_model=schemas.PlayerStatusOut)
def get_status(user_id: int = 1, db: Session = Depends(get_db)):
    stats = db.query(models.PlayerStats).filter_by(user_id=user_id).first()
    if not stats:
        # create default for demo user
        stats = models.PlayerStats(user_id=user_id, xp=0, level=1, streak=0)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return {"user_id": stats.user_id, "xp": stats.xp, "level": stats.level, "streak": stats.streak}
