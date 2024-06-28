from sqlalchemy import create_engine, Engine
from mysql.connector import connect, Error
from app.settings.settings import DATABASE_PASSWORD, DATABASE_USER, HOST
from app.database.tables.base import Base


class Database():
    '''
    База данных
    '''

    def __init__(self) -> None:

        self.database_name = "test_equipment_manager"


    def create_database(self) -> None:
        '''
        Метод для создания базы данных
        '''
        
        create_db_query = f"CREATE DATABASE {self.database_name}"
        self.__execution_request(request=create_db_query)
            

    def delete_database(self) -> None:
        '''
        Метод для удаления базы данных
        '''

        delete_request = f"DROP DATABASE {self.database_name}"
        self.__execution_request(request=delete_request)


    def __execution_request(self, request:str) -> None:
        '''
        Выполнение запроса
        '''
        try:
            with connect(
                host=HOST,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(request)
        except Error as e:
            print(e)


    def new_engine(self) -> Engine:
        '''
        Создание движка SQLalchemy
        '''

        # строка подключения
        mysql_database = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{HOST}/{self.database_name}"
        # создаем движок SqlAlchemy
        self.engine = create_engine(mysql_database, echo=False)

        self.create_table()
        return self.engine


    def create_table(self) -> None:
        '''
        Создание таблиц
        '''
        # создаем таблицы
        Base.metadata.create_all(bind=self.engine)
