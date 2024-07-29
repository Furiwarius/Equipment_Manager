import logging as log
import logging.config
from app.clients.email_client.email_client import EmailClient
import functools 
from app.settings.settings import db_log_setting
from datetime import datetime



class DatabaseLogger():
    '''
    Логгер базы данных   

    Имеет 3 режима работы: печатает в консоль,
    записывает в файл app/loggers/database_logger/logs/database.log,
    отключен.
    '''
    
    if db_log_setting.SEND_BY_MAIL:
        sender = EmailClient() 


    def get_logger(self) -> log.StreamHandler|log.FileHandler|log.NullHandler:
        '''
        Возвращает логгер с нужным режимом работы
        '''

        if db_log_setting.OPERATING_MODE=='write':
            self._setting_logger(db_log_setting.FILE_SETTING)
            self.logger = log.getLogger('write')

        elif db_log_setting.OPERATING_MODE=='print':
            self._setting_logger(db_log_setting.FILE_SETTING)
            self.logger = log.getLogger('print')

        elif db_log_setting.OPERATING_MODE=='off':
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
                
                if db_log_setting.SEND_BY_MAIL:
                    # Отправка на почту отчета об ошибке
                    self.sender.send(user_to=db_log_setting.DEVELOPER_EMAIL, 
                                    message=f"{datetime.now()} method: {func.__name__} : {err}",
                                    template=db_log_setting.REPORT_TEMPLATE)
                raise err

        return wrapper