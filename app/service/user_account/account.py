from app.utilities.hashing import to_hash
from app.service.verification_code.code import SenderCode
from app.database.crud.accountCRUD import AccountCRUD
from app.errors.service_error.account_error import (IncorrectLogin, IncorrectPassword, 
                                                    LoginExists, CodeDoesntMatch, EmailExists)
from tzlocal import get_localzone
from app.entities.account import Account


class AccountManager():
    

    def __init__(self, login:str, password:str, email:str=None) -> None:

        self.account_crud = AccountCRUD()

        if email:
            self.create(login, password, email)
        else:
            self.account = self.is_correct(login, password)
        


    def is_correct(self, login:str, password:str) -> Account:
        '''
        Сравнение данных
        '''
        acc = self.account_crud.get_account_by_login(to_hash(login))
        
        if acc is None:
            # Если логина нет в бд
            raise IncorrectLogin
        
        elif acc.password is to_hash(password):
            # Если пароль не совпадает с тем, который сохранен в бд
            raise IncorrectPassword

        return acc
    


    def change_password(self, login:str, new_password:str) -> None:
        '''
        Измненение пароля
        '''



    def create(self, login:str, password:str, email:str) -> None:
        '''
        Создание аккаунта
        '''

        if self.account_crud.get_account_by_login(to_hash(login)):
            # Если логин есть в БД
            raise LoginExists
        elif self.account_crud.get_account_by_email(email):
            # Если аккаунт с такой почтой уже есть
            raise EmailExists
        
        self.account = self.account_crud.add_account(login=to_hash(login), 
                                                    password=to_hash(password),
                                                    email=email,
                                                    timezone=get_localzone())
        
        # Отправка письма с проверочный кодом на почту
        self.verification(email)



    def verification(self, email:str) -> None:
        '''
        Отправка проверочного кода
        '''

        self.code = SenderCode(email)
        self.code.send_code()
    

    
    def confirmation(self, code:int) -> None:
        '''
        Подтверждение аккаунта
        '''

        if not self.code.check_code(code):
            # Если проверочный код не совпадает
            raise CodeDoesntMatch
    
        self.account_crud.confirm(self.account.id)
        

