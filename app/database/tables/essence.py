from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import Column, DateTime, Boolean
from datetime import datetime
from app.database.tables.base import Base



class ToolTable(Base):
    '''
    Модель таблицы tool
    '''
    __tablename__ = "tool"

    name = Column(String(60), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    factory_number = Column(String(60))
    start_date = Column(DateTime, default=datetime.now, nullable=False)
    end_date = Column(DateTime)


class WorkerTable(Base):
    '''
    Модель таблицы worker
    '''
    __tablename__ = "worker"

    account_id = Column(Integer, ForeignKey("account.id"))
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    phone_number = Column(String(11), nullable=False)
    job_title = Column(String(20), nullable=False)
    start_date = Column(DateTime, default=datetime.now, nullable=False)
    end_date = Column(DateTime)
    status = Column(Boolean, default=True)


class ConstructionTable(Base):
    '''
    Модель таблицы construction
    '''
    __tablename__ = "construction"

    name = Column(String(60), nullable=False)
    project = Column(String(60), nullable=False)
    address = Column(String(100), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    start_date = Column(DateTime, default=datetime.now, nullable=False)
    end_date = Column(DateTime)


class StorageTable(Base):
    '''
    Модель таблицы storage
    '''
    __tablename__ = "storage"

    name = Column(String(60), nullable=False)
    address = Column(String(100), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    start_date = Column(DateTime, default=datetime.now, nullable=False)
    end_date = Column(DateTime)


class AccountTable(Base):
    '''
    Модель таблицы account
    '''
    __tablename__ = "account"

    login = Column(String(30), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False)
    confirmation_status = Column(Boolean)