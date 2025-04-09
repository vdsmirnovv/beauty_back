from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Схема для создания пользователя
class UserCreate(BaseModel):
    telegram_id: str
    full_name: str
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True

# Схема для ответа с данными пользователя
class User(BaseModel):
    id: int
    telegram_id: str
    full_name: str
    phone_number: Optional[str] = None
    role: str

    class Config:
        orm_mode = True

# Схема для создания услуги
class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        orm_mode = True

# Схема для ответа с данными услуги
class Service(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        orm_mode = True

# Схема для создания записи (заказа)
class BookingCreate(BaseModel):
    user_id: int
    service_id: int
    slot_id: int

    class Config:
        orm_mode = True

# Схема для ответа с данными записи
class Booking(BaseModel):
    id: int
    user_id: int
    service_id: int
    slot_id: int

    class Config:
        orm_mode = True

# Схема для редактирования услуги
class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

    class Config:
        orm_mode = True

# Схема для редактирования записи
class BookingUpdate(BaseModel):
    user_id: Optional[int] = None
    service_id: Optional[int] = None
    slot_id: Optional[int] = None

    class Config:
        orm_mode = True

# --- СЛОТЫ ---
class SlotBase(BaseModel):
    date_time: datetime
    service_id: int

class SlotCreate(SlotBase):
    pass

class Slot(SlotBase):
    id: int

    class Config:
        from_attributes = True


# --- ЗАПИСИ ---
class BookingBase(BaseModel):
    user_id: int
    service_id: int
    slot_id: int

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int

    class Config:
        from_attributes = True