from datetime import datetime
import enum

class ToolStatus(enum.Enum):
    '''
    Описание статуса инструмента
    '''
    # Работает
    works = True
    # Сломан
    faulty = False


class Tool():
    '''
    Инструмент

    Для обхода ошибки взаимного импорта описание возвращаемого объекта
    не указано у полейи __construction.
    При создании экземпляра класса Tool эти поля заполняются 
    методами get_construction
    Возвращаемые значение у этих методов также не указаны.
    '''
    
    def __init__(self, name:str) -> None:
        # Название инструмента
        self.__name = name
        # дата перемещения
        self.__import_date = datetime.now()
        self.__status = ToolStatus.works

        # для обхода ошибки взаимного импорта описание возвращаемого объекта не указано
        # при создании экземпляра класса Tool, 
        # эти поля заполняются методами get_construction

        # Объект на котором находится инструмент
        self.__construction = None

    
    def __nonzero__(self) -> bool:
        return self.__status
    

    def __str__(self) -> str:
        return self.__name

    
    # для обхода ошибки взаимного импорта описание возвращаемого объекта не указано
    # возвращаемыый класс Сonstruction
    def get_construction(self):

        return self.__construction
    

    def get_import_date(self) -> datetime:
        return self.__import_date


    # ВАЖНО! Так как, валидация данных происходит в другом классе,
    # в методах изменения она отсутствует

    def change_import_date(self, new_date:datetime) -> None:
        '''
        Измененние даты перемещения инструмента
        '''
        self.__import_date = new_date


    def change_construction(self, new_construction) -> None:
        '''
        Изменение объекта, на котором находится инструмент
        '''
        self.__construction = new_construction


    def break_tool(self):
        '''
        Сломать инструмент
        '''
        self.__status = ToolStatus.faulty
    

    def fix_tool(self):
        '''
        Починить инструмент
        '''
        self.__status = ToolStatus.works