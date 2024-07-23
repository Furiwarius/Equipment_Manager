from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import Column, DateTime, Boolean
from datetime import datetime
from app.database.tables.base import Base



class ToolTable(Base):
    '''
    Модель таблицы tool
    '''
    __tablename__ = "tool"

    firm_id = Column(Integer, ForeignKey("firm.id"), nullable=False)
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

    firm_id = Column(Integer, ForeignKey("firm.id"), nullable=False)
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

    firm_id = Column(Integer, ForeignKey("firm.id"), nullable=False)
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

    firm_id = Column(Integer, ForeignKey("firm.id"), nullable=False)
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
    
    login = Column(String(65), nullable=False, unique=True)
    password = Column(String(65), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    confirmation_status = Column(Boolean, default=False)
    timezone = Column(String(40), nullable=False)



class FirmTable(Base):
    '''
    Модель таблицы firm
    '''
    __tablename__ = "firm"

    name = Column(String(65), nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    start_date = Column(DateTime, default=datetime.now, nullable=False)
    end_date = Column(DateTime)