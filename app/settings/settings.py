import dotenv
import os
from functools import lru_cache


dotenv.load_dotenv()


class EmailClientSetting():
    '''
    Настройки для клиента отправляющего сообщения
    '''
    
    @lru_cache
    def __init__(self) -> None:
        
        # Почта с которой будут отправляться сообщения
        self.EMAIL = os.getenv("EMAIL")
        # Пароль приложения для автоматической отправки
        self.PASSWORD = os.getenv("PASSWORD")



class DatabaseSetting():
    '''
    Настройки для базы данных
    '''

    @lru_cache
    def __init__(self) -> None:
        
        # имя пользователя БД
        self.DATABASE_USER = os.getenv("DATABASE_USER")
        # Имя тестовой БД
        self.TEST_DATABASE = os.getenv("TEST_DATABASE")
        # Имя рабочей бд
        self.NAME_DATABASE = os.getenv("NAME_DATABASE")
        # Пароль для доступа к бд
        self.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
        # Хост на котором находится бд
        self.HOST = os.getenv("HOST")



class DatabaseLoggerSetting():
    '''
    Настройки для логирования БД
    '''

    @lru_cache
    def __init__(self) -> None:
        
        # путь к шаблону с сообщением об ошибке в работе БД
        self.REPORT_TEMPLATE = r"app\templates\error_database.txt"
        
        # Путь к файлу с настройкамии логгера для разных режимов
        self.FILE_SETTING = 'app/settings/database_log.conf'

        # Режим работы логгера
        # Может быть write, print, off
        self.OPERATING_MODE = "off"

        # Почта, на которую будут отправляться сообщения об ошибках
        self.DEVELOPER_EMAIL = os.getenv("DEVELOPER_EMAIL")
        
        # id телеграма разработчика, для отправки уведомлений об ошибках
        self.DEVELOPER_USER_ID = os.getenv("DEVELOPER_USER_ID")

        # Флаг, регулирующий отправку писем с ошибками
        # Если равен True, то ошибки отправляются на DEVELOPER_EMAIL
        self.SEND_BY_MAIL = False

        # Если равен True, то ошибки отправляются на DEVELOPER_EMAIL
        self.SEND_BY_TELEGRAM = False
        
        # Токен для бота, который будет отправлять логи
        self.TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")



db_log_setting = DatabaseLoggerSetting()
db_setting = DatabaseSetting()
email_setting = EmailClientSetting()