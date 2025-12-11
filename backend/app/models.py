from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    stats = relationship("PlayerStats", back_populates="user", uselist=False)

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255))
    base_xp = Column(Integer, default=10)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # optional creator

class HabitStatusDaily(Base):
    __tablename__ = "habit_status_daily"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    __table_args__ = (UniqueConstraint('user_id', 'habit_id', 'date', name='_user_habit_date_uc'),)

class PlayerStats(Base):
    __tablename__ = "player_stats"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak = Column(Integer, default=0)

    user = relationship("User", back_populates="stats")