from app.entities.construction import Construction
from app.entities.storage import Storage
from app.entities.tool import Tool
from app.entities.worker import Worker
from datetime import datetime


class DataValidator():
    '''
    Валидатор для отдельных полей таблиц
    '''

    # Запрещенные символы
    prohibited = ('/', '|', '!', '?', '{', '}', '[', ']',
                  '"', "'", '`', '~', '+', '=', '(', ')',
                  '*', '^', '%', '$', '#', '<', '>')


    def strings_with_number(self, string:str) -> None:
        '''
        Проверка строковых значений
        с входящими в них цифрами

        К ним относятся: Адрес, имя объекта
        или склада, номер проекта, номер договора,
        название инструмента, заводской номер инструмента
        '''
    

    def only_strings(self, string:str) -> None:
        '''
        Проверка строковых значений

        К ним относятся: Имя работника,
        фамилия работника, должность работника
        '''


    def start_date(self, date:datetime) -> None:
        '''
        Проверка даты начала работ
        '''


    def end_date(self, start_date:datetime, end_date:datetime) -> None:
        '''
        Проверка даты окончания
        '''
    

    def phone_number(self, phone:str) -> None:
        '''
        Проверка номера телефона
        '''
    

        

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