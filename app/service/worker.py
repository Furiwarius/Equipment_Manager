from datetime import datetime
import enum

class WorkerTool(enum.Enum):
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
    


class Worker():
    '''
    Работник
    '''

    def __init__(self, name:str, surname:str) -> None:
        
        # Имя
        self.__name = name
        # Фамилия
        self.__surname =surname
        # Номер телефона
        self.__phone_number = None
        # Должность работника
        self.__job_title = None
        # Дата начала работы на объекте
        self.__start_date_work = datetime.now()
        # Статус работника
        self.__status = WorkerTool.works
        # список инструментов, который закреплен за лицом
        self.__tools = []
        # Объект на котором находится ответственное лицо
        self.__construction = None


    def __nonzero__(self) -> bool:

        return self.__status
    

    def __str__(self) -> str:

        if self.__job_title:
            return f"{self.__name} {self.__surname} {self.__job_title}"
        
        return f"{self.__name}{self.__surname}"
        
    
    def get_construction(self):
        '''
        Получение объекта, на котором находится работник
        '''
        return self.__construction
    

    def get_tools(self) -> list:
        '''
        Получение списка инструментов,
        который закреплен за работником
        '''
        return self.__tools


    def get_phone_number(self) -> str:
        '''
        Получение номера работника
        '''
        return self.__phone_number
    

    def get_start_date_work(self) -> datetime:
        '''
        Получение даты начала работы на объекте
        '''
        return self.__start_date_work
    

    def add_tool(self, tool) -> None:
        '''
        Добавление инструмента
        '''
        self.__tools.append(tool)
    

    def delete_tool(self, tool) -> None:
        '''
        Удаление инструмента
        '''
        self.__tools.remove(tool)

    
    def change_job_title(self, new_job_title:str) -> None:
        '''
        Добавление должности
        '''
        self.__job_title = new_job_title

    
    def change_phone_number(self, new_number:str) -> None:
        '''
        Изменение номера телефона
        '''
        self.__phone_number = new_number


    def change_construction(self, new_construction) -> None:
        '''
        Измененние объекта,
        на котором находится работник
        '''
        self.__construction = new_construction
    

    def change_start_date_work(self, new_date:datetime) -> None:
        '''
        Изменение даты начала работы на объекте
        '''
        self.__start_date_work = new_date


    def change_status(self) -> None:
        '''
        Изменение статуса работника
        '''
        pass