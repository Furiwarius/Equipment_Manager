from app.tests.fake_data import DataGenerator
from app.database.crud.accountCRUD import AccountCRUD
from app.database.crud.firmCRUD import FirmCRUD
from app.service.user_account.account import AccountManager
from app.service.firm.firm import FirmManager
from app.errors.service_error.account_error import (IncorrectLogin, 
                                                    IncorrectPassword, 
                                                    LoginExists, 
                                                    CodeDoesntMatch, 
                                                    EmailExists)
import pytest



class TestUserRoles():
    '''
    Тестирование работы классов FirmManager и AccountManager
    '''

    generator = DataGenerator()
    
    acc_crud = AccountCRUD()
    firm_crud = FirmCRUD()



    def test_add_new_account(self):
        '''
        Тестирование метода по добавлению нового аккаунта
        '''
        new_account = self.generator.account_generate()

        account_m = AccountManager(new_account, send_code=False)

        assert account_m.account.id

    
    
    def test_add_exist_account(self):
        '''
        Тестирование метода по инициализации существующего аккаунта
        '''
        account = self.acc_crud.get_last_one()

        account_m = AccountManager(account)

        assert account.id is account_m.account.id



    def test_account_exception(self):
        '''
        Тестирование работы исключений при работе с AccuntManager
        '''
        account = self.generator.account_generate()
        AccountManager(account, send_code=False)

        with pytest.raises(LoginExists):
            new_account = self.generator.account_generate()
            new_account.login = account.login
            AccountManager(new_account, send_code=False)

        with pytest.raises(EmailExists):
            new_account = self.generator.account_generate()
            new_account.email = account.email
            AccountManager(new_account, send_code=False)

        with pytest.raises(IncorrectLogin):
            incorrect_acc = self.acc_crud.get_last_one()
            incorrect_acc.login = "another_login"
            AccountManager(incorrect_acc)

        with pytest.raises(IncorrectPassword):
            incorrect_acc = self.acc_crud.get_last_one()
            incorrect_acc.password = "another_password"
            AccountManager(incorrect_acc)



    def test_add_firm(self):
        '''
        Тестирование метода по добавлению фирмы
        '''
        new_firm = self.generator.firm_generate()
        account = self.acc_crud.get_last_one()

        firm_m = FirmManager(firm=new_firm, 
                             account_id=account.id)
        assert firm_m.firm.id

        firms = self.firm_crud.get_all(account_id=account.id)
        assert firm_m.firm.id is firms

    

    def test_give_role(self):
        '''
        Тестирование метода по выдаче роли аккаунту
        '''
