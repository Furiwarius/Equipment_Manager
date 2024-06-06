from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import Column, DateTime, Boolean
from datetime import datetime
from app.database.tables.base import Base



class ToolTable(Base):
    '''
    Модель таблицы tool
    '''
    __tablename__ = "tool"

    name = Column(String(60))
    status = Column(Boolean)
    factory_number = Column(String(60), nullable=False)


class WorkerTable(Base):
    '''
    Модель таблицы worker
    '''
    __tablename__ = "worker"

    account_id = Column(Integer, ForeignKey("account.id"))
    name = Column(String(20))
    surname = Column(String(20))
    phone_number = Column(String(11))
    job_title = Column(String(20))
    start_work = Column(DateTime, default=datetime.now)
    dismissal_work = Column(DateTime, nullable=False)
    status = Column(Boolean)


class ConstructionTable(Base):
    '''
    Модель таблицы construction
    '''
    __tablename__ = "construction"

    name = Column(String(60))
    project = Column(String(60))
    address = Column(String(100))
    status = Column(Boolean)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime, nullable=False)


class StorageTable(Base):
    '''
    Модель таблицы storage
    '''
    __tablename__ = "storage"

    name = Column(String(60))
    address = Column(String(100))
    status = Column(Boolean)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime, nullable=False)


class AccountTable(Base):
    '''
    Модель таблицы account
    '''
    __tablename__ = "account"

    login = Column(String)
    password = Column(String)
    email = Column(String(30))
    confirmation_status = Column(Boolean)