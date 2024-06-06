from mysql.connector import connect, Error
from app.settings.settings import DATABASE_PASSWORD, DATABASE_USER, HOST

def create_database():
    '''
    Метод для создания базы данных
    '''
    try:
        with connect(
            host=HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD) as connection:
            create_db_query = "CREATE DATABASE test_equipment_manager"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)