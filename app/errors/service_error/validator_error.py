from app.errors.base_exception import BaseApplicationException



class BaseValidatorException(BaseApplicationException):
    '''
    Базовое исключение родитель
    для удобного отслеживания
    '''


class PresenceNumbers(BaseValidatorException):
    '''
    Вызывается, если попытаться 
    внести сущность, в 
    имени, фамилии или должности 
    которого присутствуют цифры
    '''

    def __init__(self):
        
        message = "В строке имеются цифры"
        super().__init__(message)



class ForbiddenSymbols(BaseValidatorException):
    '''
    Вызывается, если попытаться 
    внести сущность, в атрибуте
    которого присутствуют запреденные
    символы
    '''

    def __init__(self):
        
        message = "В строке имеются запрещенные символы"
        super().__init__(message)



class NonDisplayableSymbols(BaseValidatorException):
    '''
    Вызывается, если попытаться 
    внести сущность, атрибут которого
    состоит из неотображаемых символов
    '''

    def __init__(self):
        
        message = "Переданная строка состоит из неотображаемых символов"
        super().__init__(message)
    


class NotDatetime(BaseValidatorException):
    '''
    Вызывается, если попытаться 
    внести сущность, атрибут с датой
    которого не явлется типом datetime
    '''

    def __init__(self):
        
        message = "Передан другой тип данных, не datetime"
        super().__init__(message)



class DateMismatch(BaseValidatorException):
    '''
    Вызыввется, если попытаться внести
    в столбец end_time дату более раннюю
    чем start_date
    '''

    def __init__(self):
        
        message = "Дата окончания не может быть раньше даты начала"
        super().__init__(message)



class InvalidLength(BaseValidatorException):
    '''
    Вызыввется, если попытаться внести
    атрибут неверной длинны
    '''

    def __init__(self):
        
        message = "Превышена длина для передаваемого значения"
        super().__init__(message)



class NotNumber(BaseValidatorException):
    '''
    Вызыввется, если попытаться внести
    номер состоящий не только из цифр
    '''

    def __init__(self):
        
        message = "В строке имеются не только цифры"
        super().__init__(message)



class WrongType(BaseValidatorException):
    '''
    Вызыввется, если в валидатор
    передать неправильный тип данных
    '''

    def __init__(self):
        
        message = "Валидатор получил ножиданный тип данных"
        super().__init__(message)