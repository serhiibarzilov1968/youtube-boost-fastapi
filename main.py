from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
import database
import auth
from services import youtube_analyzer

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="YouTubeBoost API",
    description="API for YouTubeBoost channel management and revival service."
)

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://0.0.0.0:8000",
    "http://0.0.0.0:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Включение роутеров
app.include_router(auth.router)
app.include_router(youtube_analyzer.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to YouTubeBoost API"}

# Включение заглушек для сервисов
# from services import image_generator, shorts_generator
# app.include_router(image_generator.router)
# app.include_router(shorts_generator.router)

