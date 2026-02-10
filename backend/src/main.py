from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.data.database import init_db
from src.framework.api.v1 import horses, jockeys, owners, participants, races

app = FastAPI(
    title="RaceTracker API",
    description="API для управления информацией о скачках",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(races.router, prefix="/api/v1")
app.include_router(jockeys.router, prefix="/api/v1")
app.include_router(horses.router, prefix="/api/v1")
app.include_router(owners.router, prefix="/api/v1")
app.include_router(participants.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup():
    await init_db()
