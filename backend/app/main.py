from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import habits, player
from .database import Base, engine

# Create DB tables (dev only; use migrations for prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="The Habit Game API")

# CORS: erlauben für lokale Entwicklung (Frontend auf http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(habits.router)
app.include_router(player.router)

@app.get("/")
def root():
    return {"message": "The Habit Game API is running!"}