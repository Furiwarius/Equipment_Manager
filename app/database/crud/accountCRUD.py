from app.entities.account import Account


class AccountCRUD():
    '''
    Класс управления бд
    '''

    def get_account(self, login:str) -> Account:
        '''
        Получение данных об аккаунте по логину
        '''
        return Account


    def add_account(self, login:str, password:str, email:str) -> None:
        '''
        Добавить аккаунт в БД
        '''