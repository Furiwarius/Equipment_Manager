from app.service.utilities.hashing import to_hash

class Account():
    
    def __init__(self, login:str, password:str, account_name:str, email:str) -> None:
        
        # логин
        self.__login = to_hash(login)
        # пароль от аккаунта
        self.__password = to_hash(password)
        # при создании аккаунта требуется почта, для отправки кода
        self.__email = to_hash(email)
        # имя аккаунта, то как система будет обращаться к пользователю
        self.__account_name = account_name


    def check_login(self, transmitted_login:str) -> bool:
        '''
        Проверка логина
        '''
        return to_hash(transmitted_login)==self.__login


    def check_password(self, transmitted_password:str) -> bool:
        '''
        Проверка пароля
        '''
        return to_hash(transmitted_password)==self.__password


    def check_email(self, transmitted_email:str) -> bool:
        '''
        Проверка электронной почты
        '''
        return to_hash(transmitted_email)==self.__email
    

    def change_password(self, new_password:str):
        '''
        Измненение пароля
        '''
        if self.__password == new_password:
            raise ValueError("Новый пароль не должен совпадать со старым")
        
        self.__password = new_password


