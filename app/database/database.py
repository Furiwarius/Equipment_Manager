from sqlalchemy import create_engine, Engine
from mysql.connector import connect, Error
from app.settings.settings import DATABASE_PASSWORD, DATABASE_USER, HOST


database_name = "test_equipment_manager"


def create_database() -> None:
    '''
    Метод для создания базы данных
    '''
    try:
        with connect(
            host=HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD) as connection:
            create_db_query = f"CREATE DATABASE {database_name}"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)


def new_engine() -> Engine:
    '''
    Создание движка SQLalchemy
    '''

    # строка подключения
    sqlite_database = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{HOST}/{database_name}"
    # создаем движок SqlAlchemy
    engine = create_engine(sqlite_database, echo=True)

    return engine