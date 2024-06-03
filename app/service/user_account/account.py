from app.utilities.hashing import to_hash
from app.service.verification_code.code import SenderCode
from app.database.accountCRUD import AccountCRUD

class Account():
    
    def __init__(self) -> None:

        pass


    def is_correct(self, login:str, password:str) -> None:
        '''
        Сравнение данных
        '''
        acc = AccountCRUD.get_account(to_hash(login))
        
        if acc is None:
            # Если логина нет в бд
            raise IncorrectLogin
        
        elif acc.password is to_hash(password):
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

        if AccountCRUD.get_account(to_hash(login)):
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
        
        AccountCRUD.add_account(self.login, self.password, self.email)
