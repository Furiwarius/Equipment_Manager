from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import Column, DateTime, Boolean
from datetime import datetime
from app.database.tables.base import Base


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
    DT_start = Column(DateTime, default=datetime.now, nullable=False)
    DT_end = Column(DateTime)


class ToolsOnConstructions(Base):
    '''
    Модель таблицы tools_on_constructions

    Эта таблица отслеживает перемещение
    инструмента на объектах строительства.
    '''
    __tablename__ = "tools_on_constructions"

    tool_id = Column(Integer, ForeignKey("tool.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("construction.id"), nullable=False)
    DT_start = Column(DateTime, default=datetime.now, nullable=False)
    DT_end = Column(DateTime)


class ToolsOnStorage(Base):
    '''
    Модель таблицы tools_on_storage

    Эта таблица отслеживает перемещение
    инструмента по складам.
    '''
    __tablename__ = "tools_on_storage"

    tool_id = Column(Integer, ForeignKey("tool.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("storage.id"), nullable=False)
    DT_start = Column(DateTime, default=datetime.now, nullable=False)
    DT_end = Column(DateTime)