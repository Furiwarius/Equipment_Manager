import logging as log
import logging.config
import enum


class ModeLogger(enum.Enum):
    '''
    Режимы работы логгера БД
    '''

    print_ = 'Печатать в консоль'
    write = 'Записывать в файл'
    disable = 'Отключить'


class DatabaseLogger():
    '''
    Логгер базы данных   

    Имеет 3 режима работы: печатает в консоль,
    записывает в файл app/loggers/database_logger/logs/database.log,
    отключен.
    '''

    log_write = 'app/settings/database_log_write.conf'
    log_print = 'app/settings/database_log_print.conf'
    

    def get_logger(self, mode:ModeLogger=ModeLogger.write) -> log.StreamHandler|log.FileHandler|log.NullHandler:
        '''
        Возвращает логгер с нужным режимом работы
        '''

        if mode is ModeLogger.write:
            self._setting_logger(self.log_write)
            self.logger = log.getLogger('root')

        elif mode is ModeLogger.print_:
            self._setting_logger(self.log_print)
            self.logger = log.getLogger('root')

        elif mode is ModeLogger.disable:
            self.logger = log.NullHandler()

        return self.logger


    def _setting_logger(self, setting:str) -> None:
        '''
        Чтение настроек для логгера базы данных
        '''

        logging.config.fileConfig(setting)

    
    def info(self, func:function):
        '''
        Выводит информацию о методе и послупающих в него данных
        '''
        def work_with_func(*args, **kwargs):
            
            if isinstance(self.logger, log.NullHandler):
                result = func(*args, **kwargs)
            else:
                self.logger.info(f"method: {func.__name__}; input date: {args} {kwargs}")
                result = func(*args, **kwargs)
                self.logger.info(f"method: {func.__name__}; output date: {result}")

            return result

        return work_with_func