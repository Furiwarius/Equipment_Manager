import logging
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

    log_setting = 'app/settings/database_log.conf'


    def __init__(self, mode:ModeLogger=ModeLogger.write) -> None:
        '''
        При инициализации ключевым аргументом для
        настройки логгера является режим работы (mode).
        '''
        
        logging.config.fileConfig(fname=DatabaseLogger.log_setting)
        
        
        if mode is ModeLogger.write:
            self.log = logging.getLogger('root')

        elif mode is ModeLogger.print_:
            self.log = logging.getLogger('print')

        elif mode is ModeLogger.disable:
            self.log = logging.NullHandler()
