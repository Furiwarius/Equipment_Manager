import logging as log
import logging.config
from app.clients.email_client.email_client import EmailClient
import functools 
from app.settings.settings import DATABASE_LOG_SETTINGS, DEVELOPER_EMAIL
from datetime import datetime



class DatabaseLogger():
    '''
    Логгер базы данных   

    Имеет 3 режима работы: печатает в консоль,
    записывает в файл app/loggers/database_logger/logs/database.log,
    отключен.
    '''

    log_setting = 'app/settings/database_log.conf'
    
    sender = EmailClient() 
    # путь к шаблону с сообщением об ошибке в работе БД
    report = r"app\templates\error_database.txt"


    def get_logger(self) -> log.StreamHandler|log.FileHandler|log.NullHandler:
        '''
        Возвращает логгер с нужным режимом работы
        '''

        if DATABASE_LOG_SETTINGS=='write':
            self._setting_logger(self.log_setting)
            self.logger = log.getLogger('write')

        elif DATABASE_LOG_SETTINGS=='print':
            self._setting_logger(self.log_setting)
            self.logger = log.getLogger('print')

        elif DATABASE_LOG_SETTINGS=='off':
            self.logger = log.NullHandler()

        return self.logger



    def _setting_logger(self, setting:str) -> None:
        '''
        Чтение настроек для логгера базы данных
        '''

        logging.config.fileConfig(setting)

    
    
    def info(self, func):
        '''
        Выводит информацию о методе и послупающих в него данных
        '''
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            
            if isinstance(self.logger, log.NullHandler):
                return func(*args, **kwargs)
            
            self.logger.info(f"method: {func.__name__}; input data: {args} {kwargs}")

            try:
                result = func(*args, **kwargs)
                self.logger.info(f"method: {func.__name__}; output data: {result}")
                return result
            
            except Exception as err:
                self.logger.error(f"method: {func.__name__} : {err}")
                
                # Отправка отчета об ошибке
                self.sender.send(user_to=DEVELOPER_EMAIL, 
                                 message=f"{datetime.now()} method: {func.__name__} : {err}",
                                 template=self.report)
                raise err

        return wrapper