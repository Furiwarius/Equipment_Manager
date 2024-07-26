from app.utilities.hashing import to_hash
from app.service.verification_code.code import SenderCode
from app.database.crud.accountCRUD import AccountCRUD
from app.errors.service_error.account_error import (IncorrectLogin, IncorrectPassword, 
                                                    LoginExists, CodeDoesntMatch, EmailExists)
from tzlocal import get_localzone
from app.entities.account import Account


class AccountManager():
    

    def __init__(self, account:Account, send_code:bool=True) -> None:
        '''
        При инициализации передается экземпляр Accaunt
        в нем обязательно должны быть логин и пароль,
        если этот аккаунт существует. Если же это новый
        аккаунт, то необходимо так же передать почту, для
        проверки уникальности.

        Атрибут send_code=True значит, что при создании
        нового аккаунта будет автоматически отправляться
        код для подтверждения аккаунта. Если False, то 
        аккаунт можно будет подтверить позже.
        '''

        self.account_crud = AccountCRUD()

        if account.id is None:
            self._new_account(account, send_code)

        else:
            self._exist_account(account)
        
    

    def _new_account(self, new_account:Account, send_code:bool) -> None:
        '''
        Операции для создания нового аккаунта
        '''
        # Сюда поступают чистые данные из слоя Api
        # поэтому необходимо перед работой перевести их в hash
        new_account.login = to_hash(new_account.login)
        new_account.password = to_hash(new_account.password)

        self._check_uniqueness(new_account)
        self._create(new_account)

        if send_code:
            # Отправка письма с проверочный кодом на почту
            self.verification(self.account.email)
    


    def _exist_account(self, account:Account) -> None:
        '''
        Операции для начала работы с существуюим аккаунтом
        '''
        # Проверка на наличие аккаунта
        self._check_exist(account)
        # Проверка на коректность введенных данных
        self._is_correct(account)

        # Так как могут передаваться не все данные,
        # то вызывается этот метод, чтобы подтянуть их из БД
        self.account = self.account_crud.get_by_id(id=account.id)



    def _check_uniqueness(self, account:Account) -> None:
        '''
        Проверка уникальности передаваемых значений
        '''
        try:
            self.account_crud.check_data(login=account.login,
                                     email=account.email)
        except Exception as err:
            raise err

    

    def _check_exist(self, account:Account) -> None:
        '''
        Проверка наличия аккаунта
        '''
        bd_acc = self.account_crud.get_by_id(account.id)

        if account.login!=bd_acc.login:
            raise IncorrectLogin
        


    def _is_correct(self, account:Account) -> None:
        '''
        Сравнение паролей из бд и переданного
        '''
        acc = self.account_crud.get_account_by_login(account.login)
        
        if acc.password!=account.password:
            # Если пароль не совпадает с тем, который сохранен в бд
            raise IncorrectPassword
    


    def change_password(self, new_password:str) -> None:
        '''
        Измненение пароля
        '''



    def _create(self, account:Account) -> None:
        '''
        Создание аккаунта
        '''
        
        self.account = self.account_crud.add(account)



    def verification(self) -> None:
        '''
        Отправка проверочного кода
        '''

        self.code = SenderCode(self.account.email)
        self.code.send_code()
    

    
    def _confirmation(self, code:int) -> None:
        '''
        Подтверждение аккаунта
        '''

        if not self.code.check_code(code):
            # Если проверочный код не совпадает
            raise CodeDoesntMatch
    
        self.account_crud.modify_status(self.account.id)
        

