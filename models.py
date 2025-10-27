from sqlalchemy import Boolean, Column, Integer, String
import database

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    # Дополнительные поля для канала (пока не используются)
    channel_id = Column(String, nullable=True)
    channel_name = Column(String, nullable=True)
