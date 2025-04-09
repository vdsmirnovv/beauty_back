from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.db import SessionLocal, engine
import app.telegram_bot
from fastapi.middleware.cors import CORSMiddleware

# Инициализация FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц в базе данных (если они ещё не существуют)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт для создания нового пользователя
@app.post("/api/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# Эндпоинт для получения списка пользователей
@app.get("/api/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)

# Эндпоинт для получения пользователя по ID
@app.get("/api/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)

@app.get("/api/users/by-telegram-id/{telegram_id}", response_model=schemas.User)
def get_user_by_telegram_id(telegram_id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Эндпоинт для создания новой услуги
@app.post("/api/services/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_service(db=db, service=service)

# Эндпоинт для получения списка услуг
@app.get("/api/services/", response_model=list[schemas.Service])
def get_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_services(db=db, skip=skip, limit=limit)

# Эндпоинт для редактирования услуги
@app.put("/api/services/{service_id}", response_model=schemas.Service)
def update_service(service_id: int, service: schemas.ServiceUpdate, db: Session = Depends(get_db)):
    return crud.update_service(db=db, service_id=service_id, service=service)

# Эндпоинт для удаления услуги
@app.delete("/api/services/{service_id}", response_model=schemas.Service)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    return crud.delete_service(db=db, service_id=service_id)

# Эндпоинт для создания записи (бронирования)
@app.post("/api/bookings/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=booking)

# Эндпоинт для получения списка записей
@app.get("/api/bookings/", response_model=list[schemas.Booking])
def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bookings(db=db, skip=skip, limit=limit)

# Эндпоинт для редактирования записи
@app.put("/api/bookings/{booking_id}", response_model=schemas.Booking)
def update_booking(booking_id: int, booking: schemas.BookingUpdate, db: Session = Depends(get_db)):
    return crud.update_booking(db=db, booking_id=booking_id, booking=booking)

# Эндпоинт для удаления записи
@app.delete("/api/bookings/{booking_id}", response_model=schemas.Booking)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    return crud.delete_booking(db=db, booking_id=booking_id)

# ---------- SLOTS ----------
@app.post("/api/slots", response_model=schemas.Slot)
def create_slot(slot: schemas.SlotCreate, db: Session = Depends(get_db)):
    return crud.create_slot(db, slot)

@app.get("/api/slots", response_model=list[schemas.Slot])
def read_slots(db: Session = Depends(get_db)):
    return crud.get_slots(db)

# ---------- BOOKINGS ----------
@app.post("/api/bookings", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db, booking)

@app.get("/api/bookings", response_model=list[schemas.Booking])
def read_bookings(db: Session = Depends(get_db)):
    return crud.get_bookings(db)

# Корневой эндпоинт
@app.get("/")
def read_root():
    return {"message": "Welcome to the Beauty Salon API!"}
