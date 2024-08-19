from app.errors.base_exception import BaseException



class ThisIsSuperAdmin(BaseException):
    '''
    Вызывается при попытке сменить роль
    super_admin на другую
    '''

    def __init__(self):
        
        message = "Попытка поменять super_admin в фирме"
        super().__init__(message)



class CannotGiveSuperadmin(BaseException):
    '''
    Вызывается при попытке назначить роль super_admin
    '''

    def __init__(self):
        
        message = "Попытка назначить роль super_admin"
        super().__init__(message)