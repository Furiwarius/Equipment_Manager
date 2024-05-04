from tool import Tool
from construction import Construction
from worker import Worker

class NonWorkingComponent(Exception):
    '''
    Вызывается, если попытаться использовать
    неактивный экземпляр класса. Для избежания вызова
    следует изменить статус используемого экземпляра 
    на рабочий.
    '''


class BlankFields(Exception):
    '''
    Вызывается, если попытаться использовать
    незаполненный экземпляр класса. Для избежания вызова
    следует заполнить пустые поля.
    '''
    

class MethodError(Exception):
    '''
    Вызывается при использовании неподходящего метода.
    '''


def checking_fields_filled(field_list:list) -> None:
        for field in field_list:
            if field==None:
                raise BlankFields("Важные поля не заполнены")            


def checking_incoming_objects(annotations:dict, obtained_values:list) -> None:
    '''
    Проверка входных данных
    '''
    checking_class(annotations=annotations, obtained_values=obtained_values)
    checking_status(obtained_values=obtained_values)
    

def checking_class(annotations:dict, obtained_values:list) -> None:
    '''
    Проверка на принадлежность передаваемых
    значений требуемым в функции классе
    '''
    for key, value in zip(annotations, obtained_values):
        if type(value)!=annotations.get(key):
            raise TypeError("Передан неиспользуемый класс")
        

def checking_status(obtained_values:list) -> None:
    '''
    Проверка статуса у передаваемых объектов
    '''
    for elem in obtained_values:
        if elem:
            continue
        raise NonWorkingComponent("Один из переданных объектов, является неактивным")