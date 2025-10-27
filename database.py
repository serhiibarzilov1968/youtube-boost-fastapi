# database.py - Полная версия

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Настройка подключения к базе данных ---

# Мы будем использовать SQLite, которая хранит базу данных в одном файле.
# Этот файл будет называться youtube_boost.db и появится в вашей папке проекта.
SQLALCHEMY_DATABASE_URL = "sqlite:///./youtube_boost.db"

# Создаем "движок" SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # Этот параметр нужен только для SQLite, чтобы разрешить использование в разных потоках
    connect_args={"check_same_thread": False} 
)

# Создаем фабрику сессий, через которую мы будем общаться с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для наших моделей (таблиц)
Base = declarative_base()

# --- Функция-зависимость для получения сессии ---
# Мы перенесли ее сюда из main.py, чтобы все было в одном месте
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
