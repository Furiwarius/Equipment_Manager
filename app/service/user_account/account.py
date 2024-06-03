from app.utilities.hashing import to_hash
from app.service.verification_code.code import SenderCode

class Account():
    
    def __init__(self) -> None:

        pass


    def is_correct(self, login:str, password:str) -> None:
        '''
        Сравнение данных
        '''

        if AccountCRUD.is_login_correct(to_hash(login)) is None:
            # Если логина нет в бд
            raise IncorrectLogin
        
        elif not AccountCRUD.is_password_correct(login, 
                                             to_hash(password)):
            # Если пароль не совпадает с тем, который сохранен в бд
            raise IncorrectPassword
    

    def change_password(self, login:str, new_password:str) -> None:
        '''
        Измненение пароля
        '''


    def create(self, login:str, password:str, email:str) -> None:
        '''
        Создание аккаунта
        '''

        if AccountCRUD.is_login_correct(to_hash(login)):
            # Если логин есть в БД
            raise LoginExists
        
        self.login = login
        self.password = password
        self.email = email
        
        self.verification()


    def verification(self) -> None:
        '''
        Отправка проверочного кода
        '''

        self.code = SenderCode(self.email)
        self.code.send_code()
    
    
    def confirmation(self, code:int) -> None:
        '''
        Подтверждение аккаунта
        '''

        if not self.code.check_code(code):
            # Если проверочный код не совпадает
            raise CodeDoesntMatch
        
        AccountCRUD.add_account(login, password, email)
