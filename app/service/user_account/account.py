from app.utilities.hashing import to_hash
from app.service.verification_code.code import SenderCode
from app.database.crud.accountCRUD import AccountCRUD
from app.errors.service_error.account_error import IncorrectLogin, IncorrectPassword, LoginExists, CodeDoesntMatch
from tzlocal import get_localzone


class AccountManager():
    

    def __init__(self, login:str, password:str, email:str=None) -> None:
        self.account_crud = AccountCRUD()

        if email:
            self.create(login, password, email)
        else:
            self.is_correct(login, password)
        


    def is_correct(self, login:str, password:str) -> None:
        '''
        Сравнение данных
        '''
        acc = self.account_crud.get_account(to_hash(login), to_hash(password))
        
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

        # ДОРАБОТАТЬ ПРОВЕРКУ ЛОГИНА И ПОЧТЫ
        if self.account_crud.get_account(to_hash(login), to_hash(password)):
            # Если логин есть в БД
            raise LoginExists
        
        self.account_crud.add_account(login=to_hash(login), 
                                        password=to_hash(password),
                                        email=email,
                                        timezone=get_localzone())
        
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
        

