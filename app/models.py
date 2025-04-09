from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    full_name = Column(String(20))  # Имя до 20 символов
    phone_number = Column(String, nullable=True)  # Телефонный номер
    role = Column(String, default="user")  # Роль по умолчанию

    WHITELISTED_TELEGRAM_IDS = ["878443461", "596691093"]  # Белый список

    bookings = relationship("Booking", back_populates="user")

    def assign_role(self):
        if self.telegram_id in self.WHITELISTED_TELEGRAM_IDS:
            self.role = "admin"
        else:
            self.role = "user"

    def __init__(self, telegram_id, full_name, phone_number=None):
        self.telegram_id = telegram_id
        self.full_name = full_name
        self.phone_number = phone_number
        self.assign_role()

    def __repr__(self):
        return f"User(id={self.id}, full_name={self.full_name}, telegram_id={self.telegram_id}, role={self.role})"
    
class Service(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)  
    description = Column(String(250), nullable=True) 
    price = Column(Float, nullable=False)  
    image_url = Column(String(255), nullable=True)  
    category = Column(String(50), nullable=True)  
    
    bookings = relationship("Booking", back_populates="service")
    slots = relationship("Slot", back_populates="service")

class Slot(Base):
    __tablename__ = 'slots'
    
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, unique=True)
    service_id = Column(Integer, ForeignKey('services.id'))
    
    service = relationship("Service", back_populates="slots")
    bookings = relationship("Booking", back_populates="slot")

class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    slot_id = Column(Integer, ForeignKey('slots.id'))
    
    user = relationship("User", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")
    slot = relationship("Slot", back_populates="bookings")