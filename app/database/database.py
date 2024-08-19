from sqlalchemy import create_engine, Engine
from mysql.connector import connect, Error
from app.settings.settings import db_setting
from app.database.tables.base import Base
from sqlalchemy.orm import Session


class Database():
    '''
    База данных

    Имеет всего 1 экземпляр на все приложение
    '''
    # Переменная с именем БД
    database_name = db_setting.TEST_DATABASE


    _instance = None  # Приватное поле для хранения единственного экземпляра


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._new_engine()
            cls._instance._create_table()
        return cls._instance
    


    def __enter__(self) -> Session:
        self.__new__(self)
        with Session(autoflush=False, bind=self.engine) as db:
            self.session = db
            return self.session


    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.session:
            self.session.close()




    def create_database(self) -> None:
        '''
        Метод для создания базы данных
        '''
        
        create_db_query = f"CREATE DATABASE {self.database_name}"
        self._execution_request(request=create_db_query)
            


    def delete_database(self) -> None:
        '''
        Метод для удаления базы данных
        '''

        delete_request = f"DROP DATABASE {self.database_name}"
        self._execution_request(request=delete_request)



    def _execution_request(self, request:str) -> None:
        '''
        Выполнение запроса
        '''
        try:
            with connect(
                host=db_setting.HOST,
                user=db_setting.DATABASE_USER,
                password=db_setting.DATABASE_PASSWORD) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(request)
        except Error as e:
            print(e)



    def _new_engine(self) -> Engine:
        '''
        Создание движка SQLalchemy
        '''
        self.create_database()
        # строка подключения
        mysql_database = f"mysql+pymysql://{db_setting.DATABASE_USER}:{db_setting.DATABASE_PASSWORD}@{db_setting.HOST}/{self.database_name}"
        # создаем движок SqlAlchemy
        self.engine = create_engine(mysql_database, echo=False)



    def _create_table(self) -> None:
        '''
        Создание таблиц
        '''
        # создаем таблицы
        Base.metadata.create_all(bind=self.engine)
