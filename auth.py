from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas
import models
import database

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # In a real application, you would hash the password here
    
    new_user = models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    # 1. Проверка существования пользователя
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials (User not found)")
    
    # 2. Проверка пароля (в реальном приложении - проверка хеша)
    if db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials (Wrong password)")
    
    # 3. Успешный вход - возвращаем токен (заглушку)
    # В реальном приложении здесь будет генерация JWT токена
    return {"message": "Login successful", "access_token": "fake_jwt_token_for_user_" + str(db_user.id), "token_type": "bearer"}

