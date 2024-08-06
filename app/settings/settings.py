import dotenv
import os
from datetime import timedelta

dotenv.load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DATABASE_USER = os.getenv("DATABASE_USER")
TEST_DATABASE = os.getenv("TEST_DATABASE")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
HOST = os.getenv("HOST")
DATABASE_LOG_SETTINGS = os.getenv("DATABASE_LOG_SETTINGS")
DEVELOPER_EMAIL = os.getenv("DEVELOPER_EMAIL")


class JWTSettings():
    '''
    Настройки для работы с токенами
    '''

    JWT_KEY = os.getenv("JWT_KEY")

    ALGORITHM = "HS256"

    EXPIRATION_TIME = timedelta(minutes=30)


class ApplicationSetting():
    '''
    Настройки приложения
    '''

    favicon_path = 'app/static/img/favicon.ico'


jwt_settings = JWTSettings()
app_settings = ApplicationSetting()