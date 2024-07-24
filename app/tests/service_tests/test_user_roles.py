from app.tests.fake_data import DataGenerator
from app.database.crud.accountCRUD import AccountCRUD
from app.database.crud.firmCRUD import FirmCRUD
from app.service.user_account.account import AccountManager



class TestUserRoles():
    '''
    Тестирование работы классов FirmManager и AccountManager
    '''

    generator = DataGenerator()
    
    app_crud = AccountCRUD()
    firm_crud = FirmCRUD()



    def test_add_account(self):
        '''
        Тестирование метода по добавлению аккаунта
        '''
        new_account = self.generator.account_generate()
        account_M = AccountManager(login=new_account.login,
                                   password=new_account.password,
                                   email=new_account.email)




    def test_is_correct(self):
        '''
        Тестирование метода AcoountManager.is_correct()
        '''
        new_account = self.generator.account_generate()
        account = self.app_crud.add(new_account)



    

    def test_add_firm(self):
        '''
        Тестирование метода по добавлению фирмы
        '''
    

    def test_give_role(self):
        '''
        Тестирование метода по выдаче роли аккаунту
        '''

    
    
    
