from datetime import datetime
import enum


class ConstructionStatus(enum.Enum):
    '''
    Статус объекта
    '''
    under_construction = True
    stopped = True
    finished = False

class Construction():
    '''
    Объект

    Для обхода ошибки взаимного импорта описание возвращаемого объекта
    не указано у полей __responsible.
    При создании экземпляра класса Сonstruction это поле заполняется 
    методом get_responsible. 
    Возвращаемые и получаемые значения у методов, связанных с этими полями не указаны.
    '''
    
    def __init__(self, name:str, project:str) -> None:
        
        # название объекта
        self.__name = name
        # номер проекта или договора подряда
        self.__project = project

        # Ответственное лицо, отвечающее за объект строительства
        self.__responsible = None
        # список инструментов
        self.__tools = []
        # статус объекта
        self.__status = ConstructionStatus.under_construction
        # дата создания
        self.__date_creation = datetime.now()


    def __nonzero__(self) -> bool:
        return {self.__status}
    

    def __str__(self) -> str:
        return f"{self.__name} {self.__project}"


    def get_tools(self) -> list:
        '''
        Получение списка инструментов
        '''
        return self.__tools


    # для обхода ошибки взаимного импорта описание возвращаемого объекта не указано
    # возвращаемыый класс Worker
    def get_responsible(self):
        '''
        Получение ответственного лица на данном объекте
        '''
        return self.__responsible
    

    def get_date_creation(self) -> datetime:
        '''
        Получение даты начала работ на объекте
        '''
        return self.__date_creation
    

    # ВАЖНО! Так как, валидация данных происходит в другом классе,
    # в методах изменения она отсутствует


    def add_tool(self, new_tool) -> None:
        '''
        Добавление инструмента
        '''
        self.__tools.append(new_tool)


    def tool_check(self, tools:list) -> bool:
        '''
        Проверка наличия инструмента
        '''
        for tool in tools:
            if tool not in self.__tools:
                return False
        return True
            
    
    def delete_tool(self, remove_tool) -> None:
        '''
        Удаление инструмента
        '''
        self.__tools.remove(remove_tool)


    def change_responsible(self, new_responsible) -> None:
        '''
        Изменение ответственного лица
        '''
        self.__responsible = new_responsible
    

    def change_date_creation(self, new_date:datetime) -> None:
        '''
        Изменение даты начала работ на объекте
        '''
        self.__date_creation = new_date


    def change_name(self, new_name:str) -> None:
        '''
        Изменение названия объекта
        '''
        self.__name = new_name
    

    def change_project(self, new_project:str) -> None:
        '''
        Изменение номера проекта или договора
        '''
        self.__project = new_project