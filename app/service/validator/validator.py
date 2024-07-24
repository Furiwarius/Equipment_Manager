from app.entities.construction import Construction
from app.entities.storage import Storage
from app.entities.tool import Tool
from app.entities.worker import Worker
from app.entities.account import Account
from app.entities.firm import Firm
from datetime import datetime
from app.errors.service_error.validator_error import PresenceNumbers, ForbiddenSymbols
from app.errors.service_error.validator_error import NonDisplayableSymbols, NotDatetime
from app.errors.service_error.validator_error import DateMismatch, NotNumber
from app.errors.service_error.validator_error import WrongType, InvalidLength


class DataValidator():
    '''
    Валидатор для отдельных полей таблиц
    '''

    # Запрещенные символы
    prohibited = '''|!?}{[]"'`~+=*^%$#<>'''


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



    def end_date(self, start_date:datetime, end_date:datetime|None) -> None:
        '''
        Проверка даты окончания
        '''
        if end_date:
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

    valid = DataValidator()


    def validate_construction(self, constr: Construction) -> None:
        '''
        Валидатор для новой записи
        в таблицу construction 
        '''

        if not isinstance(constr, Construction):
            raise WrongType
        
        self.valid.only_strings(constr.name, length=60)
        self.valid.strings_with_number(constr.address, length=100)
        self.valid.strings_with_number(constr.project, length=60)
        self.valid.start_date(constr.start_date)
        self.valid.end_date(constr.start_date, constr.end_date)
        


    def validate_storage(self, storage:Storage) -> None:
        '''
        Валидатор для новой записи
        в таблицу storage 
        '''

        if not isinstance(storage, Storage):
            raise WrongType

        self.valid.only_strings(storage.name, length=60)
        self.valid.strings_with_number(storage.address, length=100)
        self.valid.start_date(storage.start_date)
        self.valid.end_date(storage.start_date, storage.end_date)



    def validate_tool(self, tool:Tool) -> None:
        '''
        Валидатор для новой записи
        в таблицу tool
        '''

        if not isinstance(tool, Tool):
            raise WrongType
        
        self.valid.only_strings(tool.name, length=60)
        self.valid.strings_with_number(tool.factory_number, length=60)
        self.valid.start_date(tool.start_date)
        self.valid.end_date(tool.start_date, tool.end_date)



    def validate_worker(self, worker:Worker) -> None:
        '''
        Валидатор для новой записи
        в таблицу worker 
        '''

        if not isinstance(worker, Worker):
            raise WrongType
        
        self.valid.only_strings(worker.name, length=20)
        self.valid.only_strings(worker.surname, length=20)
        self.valid.phone_number(worker.phone_number)
        self.valid.only_strings(worker.job_title, length=40)
        self.valid.start_date(worker.start_date)
        self.valid.end_date(worker.start_date, worker.end_date)


    
    def validate_account(self, account:Account) -> None:
        '''
        Валидатор для новой записи
        в таблицу account
        '''

    
    
    def validate_firm(self, firm:Firm) -> None:
        '''
        Валидатор для новой записи
        в таблицу firm
        '''