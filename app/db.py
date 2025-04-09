
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Строка подключения к базе данных
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:uftHgAOGeXIkjAIRjkVuBwjqvSETmdzM@crossover.proxy.rlwy.net:12938/railway"

# Создаём движок подключения (без параметра check_same_thread)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаём сессию для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей
Base = declarative_base()

