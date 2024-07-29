import dotenv
import os

dotenv.load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DATABASE_USER = os.getenv("DATABASE_USER")
TEST_DATABASE = os.getenv("TEST_DATABASE")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
HOST = os.getenv("HOST")



class DatabaseLoggerSetting():
    '''
    Настройки для логирования БД
    '''
    # путь к шаблону с сообщением об ошибке в работе БД
    REPORT_TEMPLATE = r"app\templates\error_database.txt"
    
    # Путь к файлу с настройкамии логгера для разных режимов
    FILE_SETTING = 'app/settings/database_log.conf'

    # Режим работы логгера
    # Может быть write, print, off
    OPERATING_MODE = "off"

    # Почта, на которую будут отправляться сообщения об ошибках
    DEVELOPER_EMAIL = os.getenv("DEVELOPER_EMAIL")

    # Флаг, регулирующий отправку писем с ошибками
    # Если равен True, то ошибки отправляются на DEVELOPER_EMAIL
    SEND_BY_MAIL = False



db_log_setting = DatabaseLoggerSetting()