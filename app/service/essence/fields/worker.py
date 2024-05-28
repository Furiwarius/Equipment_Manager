from datetime import datetime
from dataclasses import dataclass
import enum

class StatusWorker(enum.Enum):
    '''
    Статус работника
    '''
    # Работает
    works = True
    # Уволен
    fired = False
    # В отпуске
    on_holiday = False
    # болеет
    sick = False
    

@dataclass
class Worker():
    '''
    Работник
    '''

    id: int
    # Имя
    name: str
    # Фамилия
    surname: str
    # Номер телефона
    phone_number: int
    # Должность работника
    job_title: str
    # Дата начала работы на объекте
    start_work: datetime
    # Статус работника
    status: StatusWorker
    # Id объекта, на котором работник ответветственный
    # Изначально None, тк работник
    # может просто храниться в бд 
    # и не находится на объете
    # В бд этот атрибут хранится не будет
    construction: int = None
    

    def __str__(self) -> str:
        if self.job_title:
            return f"{self.name} {self.surname} {self.job_title}"
        
        return f"{self.name}{self.surname}"
        
    
    def get_id(self) -> int:
        '''
        Получение id
        '''
        return self.id


    def get_status(self) -> StatusWorker:
        '''
        Получение статуса работника
        '''
        return self.status


    def get_phone_number(self) -> str:
        '''
        Получение номера работника
        '''
        return self.phone_number
    

    def get_date_work(self) -> datetime:
        '''
        Получение даты начала работы на объекте
        '''
        return self.start_work


    def get_construction(self) -> int:
        '''
        Получить объект, за который отвечает этот работник

        Возвращает None, если не прикреплен к объекту
        '''

        return self.construction

    
    def change_title(self, new_job_title:str) -> None:
        '''
        Добавление должности
        '''
        self.job_title = new_job_title

    
    def change_phone(self, new_number:str) -> None:
        '''
        Изменение номера телефона
        '''
        self.phone_number = new_number
    

    def change_date_work(self, new_date:datetime) -> None:
        '''
        Изменение даты начала работы на объекте
        '''
        self.start_work = new_date


    def get_sick(self) -> None:
        '''
        Работник заболевает
        '''
        self.status = StatusWorker.sick  


    def dismiss(self) -> None:
        '''
        Уволить работника
        '''
        self.status = StatusWorker.fired
        self.construction = None
        

    def get_well(self) -> None:
        '''
        Работник выздоравливает
        '''     
        self.status = StatusWorker.works


    def change_construction(self, construction: int = None) -> None:
        '''
        Сменить объект

        Если необходимо удалить объект у работника,
        то вызывается этот метод без атрибутов
        '''
        self.construction = construction
