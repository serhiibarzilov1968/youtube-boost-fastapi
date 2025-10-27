from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, auth
from .services import youtube_analyzer

# Создание базы данных (если не существует)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="YouTubeBoost API",
    description="API для анализа и продвижения YouTube каналов."
)

# Настройка CORS
origins = [
    "http://localhost:8000",  # Разрешаем фронтенду на 8000
    "http://127.0.0.1:8000",
    # Добавьте здесь адрес вашего хостинга (например, "https://youtube-boost.onrender.com" )
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
# from .services import image_generator, shorts_generator
# app.include_router(image_generator.router)
# app.include_router(shorts_generator.router)
