from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import Column, DateTime, Boolean
from datetime import datetime
from app.database.tables.base import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class WorksOnConstructions(Base):
    '''
    Модель таблицы works_on_constructions

    Эта таблица отслеживает нахождение работников на объектах.
    А также ответственных лиц на этих объектах.
    '''
    __tablename__ = "works_on_constructions"

    worker_id = Column(Integer, ForeignKey("worker.id"), nullable=False)
    construction_id = Column(Integer, ForeignKey("construction.id"), nullable=False)
    is_brigadir = Column(Boolean, nullable=False)
    start_date = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False)
    end_date = Column(DateTime)


class ToolsOnConstructions(Base):
    '''
    Модель таблицы tools_on_constructions

    Эта таблица отслеживает перемещение
    инструмента на объектах строительства.
    '''
    __tablename__ = "tools_on_constructions"

    tool_id = Column(Integer, ForeignKey("tool.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("construction.id"), nullable=False)
    start_date = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False)
    end_date = Column(DateTime)


class ToolsOnStorage(Base):
    '''
    Модель таблицы tools_on_storage

    Эта таблица отслеживает перемещение
    инструмента по складам.
    '''
    __tablename__ = "tools_on_storage"

    tool_id = Column(Integer, ForeignKey("tool.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("storage.id"), nullable=False)
    start_date = Column(DateTime, default=func.now(), server_default=func.now(), nullable=False)
    end_date = Column(DateTime)



class AccountRoles(Base):
    '''
    Модель таблицы account_roles
    
    Отслеживает роли аккаунтов в фирмах.
    Существует 3 роли: супер админ (владелец),
    админ (назначает супер админ), посетитель 
    (назначает супер админ)
    '''

    __tablename__ = "account_roles"

    firm_id = Column(Integer, ForeignKey("firm.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    role = Column(String(16), nullable=False)

    account = relationship("AccountTable", back_populates="firms")
    firm = relationship("FirmTable", back_populates="accounts")