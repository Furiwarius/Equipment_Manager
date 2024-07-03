from app.entities.construction import Construction
from app.entities.storage import Storage
from app.entities.tool import Tool
from app.entities.worker import Worker
from datetime import datetime
from app.errors.service_error.validator_error import PresenceNumbers, ForbiddenSymbols
from app.errors.service_error.validator_error import NonDisplayableSymbols, NotDatetime
from app.errors.service_error.validator_error import DateMismatch, NotNumber, InvalidLength



class DataValidator():
    '''
    Валидатор для отдельных полей таблиц
    '''

    # Запрещенные символы
    prohibited = '''/|!?}{[]"'`~+=()*^%$#<>'''


    def strings_with_number(self, string:str, length=0) -> None:
        '''
        Проверка строковых значений
        с входящими в них цифрами

        К ним относятся: Адрес, имя объекта
        или склада, номер проекта, номер договора,
        название инструмента, заводской номер инструмента
        '''

        symbols = set(string)

        if not symbols.isdisjoint(set(self.prohibited)):
            raise ForbiddenSymbols

        elif string.isspace():
            raise NonDisplayableSymbols

        # Если задана необходимая длина строки
        elif length and len(string)>length:
            raise InvalidLength
    


    def only_strings(self, string:str, length=0) -> None:
        '''
        Проверка строковых значений

        К ним относятся: Имя работника,
        фамилия работника, должность работника
        '''

        nummers = set(range(10))
        symbols = set(string)

        if not symbols.isdisjoint(nummers):
            raise PresenceNumbers
        
        elif not symbols.isdisjoint(set(self.prohibited)):
            raise ForbiddenSymbols
        
        elif string.isspace():
            raise NonDisplayableSymbols

        # Если задана необходимая длина строки
        elif length and len(string)>length:
            raise InvalidLength



    def start_date(self, date:datetime) -> None:
        '''
        Проверка даты начала работ
        '''

        if not isinstance(date, datetime):
            raise NotDatetime



    def end_date(self, start_date:datetime, end_date:datetime) -> None:
        '''
        Проверка даты окончания
        '''

        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise NotDatetime
        
        elif end_date<start_date:
            raise DateMismatch
    


    def phone_number(self, phone:str) -> None:
        '''
        Проверка номера телефона
        '''

        if not phone.isdigit():
            raise NotNumber

        elif len(phone) != 11:
            raise InvalidLength

        

class ValidatorEssence():
    '''
    Валидатор поступающих в БД данных
    '''

    validator = DataValidator()


    def validate_construction(self, constr: Construction) -> bool:
        '''
        Валидатор для новой записи
        в таблицу construction 
        '''
    

    def validate_storage(self, storage:Storage) -> bool:
        '''
        Валидатор для новой записи
        в таблицу storage 
        '''
    

    def validate_tool(self, tool:Tool) -> bool:
        '''
        Валидатор для новой записи
        в таблицу tool
        '''


    def validate_worker(self, worker:Worker) -> bool:
        '''
        Валидатор для новой записи
        в таблицу worker 
        '''