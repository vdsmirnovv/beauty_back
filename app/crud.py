from sqlalchemy.orm import Session
from app import models, schemas

# --- Пользователи ---
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        telegram_id=user.telegram_id,
        full_name=user.full_name,
        phone_number=user.phone_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# --- Услуги ---
def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(
        name=service.name,
        description=service.description,
        price=service.price
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).offset(skip).limit(limit).all()

def update_service(db: Session, service_id: int, service: schemas.ServiceCreate):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service:
        db_service.name = service.name
        db_service.description = service.description
        db_service.price = service.price
        db.commit()
        db.refresh(db_service)
    return db_service

def delete_service(db: Session, service_id: int):
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service:
        db.delete(db_service)
        db.commit()
    return db_service

# --- Слоты ---
def create_slot(db: Session, slot: schemas.SlotCreate):
    db_slot = models.Slot(
        date_time=slot.date_time,
        service_id=slot.service_id
    )
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

def get_slots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Slot).offset(skip).limit(limit).all()

# --- Записи (бронь) ---
def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = models.Booking(
        user_id=booking.user_id,
        service_id=booking.service_id,
        slot_id=booking.slot_id
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()
