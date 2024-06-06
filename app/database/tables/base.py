from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer

class Base(DeclarativeBase):
    '''
    Базовый класс для моделей
    '''
    id = Column(Integer, primary_key=True, 
                index=True, autoincrement='auto', unique=True)