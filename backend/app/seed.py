# Run once to fill DB with sample user & habits
from .database import SessionLocal, engine
from . import models

def seed():
    db = SessionLocal()
    # create default user if not exists
    user = db.query(models.User).filter_by(username="demo").first()
    if not user:
        user = models.User(username="demo", password_hash="demo")  # demo only; no real hashing here
        db.add(user)
        db.commit()
        db.refresh(user)
    # sample habits
    if db.query(models.Habit).count() == 0:
        h1 = models.Habit(title="Wasser trinken", description="1 Glas Wasser", base_xp=10, created_by=user.id)
        h2 = models.Habit(title="5 Minuten Stretching", description="Kurz dehnen", base_xp=15, created_by=user.id)
        db.add_all([h1, h2])
        db.commit()
    db.close()

if __name__ == "__main__":
    seed()
    print("Seeding complete.")
