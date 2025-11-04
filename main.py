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
    "http://127.0.0.1:8000",
    "https://youtube-boost-fastapi-06e21a623f18.herokuapp.com", # Ваш Heroku URL бэкенда
    "https://youtube-boost-frontend-2025-0a8da5262657.herokuapp.com" # <-- Ваш Heroku URL фронтенда
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

