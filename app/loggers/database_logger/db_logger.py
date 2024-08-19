import logging as log
import logging.config
from app.clients.email_client.email_client import EmailClient
import functools 
from app.settings.settings import db_log_setting
from datetime import datetime
from app.clients.telegram_client.tg_client import TelegramClient



class DatabaseLogger():
    '''
    Логгер базы данных   

    Имеет 3 режима работы: печатает в консоль,
    записывает в файл app/loggers/database_logger/logs/database.log,
    отключен.
    '''
    
    if db_log_setting.SEND_BY_MAIL:
        email_sender = EmailClient() 

    if db_log_setting.SEND_BY_TELEGRAM:
        tg_sender = TelegramClient()


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
                
                message = f"{datetime.now()} method: {func.__name__} : {err}"
                self._send_message_for_email(message)
                self._send_message_for_telergam(message)
                
                raise err

        return wrapper
    


    def _send_message_for_telergam(self, message:str) -> None:
        '''
        Отправка уведомления об ошибке в телеграм
        '''
        if db_log_setting.SEND_BY_TELEGRAM:
                    # Отправка сообщения в телеграм
                    self.tg_sender.send(message)
    


    def _send_message_for_email(self, message:str) -> None:
        '''
        Отправка уведомления об ошибке на почту
        '''
        if db_log_setting.SEND_BY_MAIL:
                    # Отправка на почту отчета об ошибке
                    self.email_sender.send(user_to=db_log_setting.DEVELOPER_EMAIL, 
                                    message=message,
                                    template=db_log_setting.REPORT_TEMPLATE)
