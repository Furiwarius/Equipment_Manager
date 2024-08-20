from app.tests.fake_data import DataGenerator
from app.database.crud.accountCRUD import AccountCRUD, Account
from app.database.crud.firmCRUD import FirmCRUD, Roles
from app.service.user_account.account import AccountManager
from app.service.firm.firm import FirmManager, Firm
from app.errors.service_error.account_error import (IncorrectLogin, 
                                                    IncorrectPassword, 
                                                    LoginExists, 
                                                    CodeDoesntMatch, 
                                                    EmailExists)
import pytest
from copy import copy



class TestUserRoles():
    '''
    Тестирование работы классов FirmManager и AccountManager
    '''

    generator = DataGenerator()
    
    acc_crud = AccountCRUD()
    firm_crud = FirmCRUD()



    def test_add_new_account(self, account:Account):
        '''
        Тестирование метода по добавлению нового аккаунта
        '''

        account_m = AccountManager(account, send_code=False, new=True)

        assert account_m.account.id

    
    
    def test_add_exist_account(self, account:Account, acc_crud:AccountCRUD):
        '''
        Тестирование метода по инициализации существующего аккаунта
        '''

        AccountManager(copy(account), send_code=False, new=True)

        account_m = AccountManager(copy(account), send_code=False)

        assert acc_crud.get_last_one().id is account_m.account.id


    @pytest.mark.skip()
    def test_account_exception(self, account:Account, acc_crud:AccountCRUD):
        '''
        Тестирование работы исключений при работе с AccuntManager
        '''
        account = self.generator.account_generate()
        AccountManager(copy(account), send_code=False, new=True)

        with pytest.raises(LoginExists):
            new_account = self.generator.account_generate()
            new_account.login = account.login
            AccountManager(new_account, send_code=False, new=True)

        with pytest.raises(EmailExists):
            new_account = self.generator.account_generate()
            new_account.email = account.email
            AccountManager(new_account, send_code=False, new=True)

        with pytest.raises(IncorrectLogin):
            incorrect_acc = copy(account)
            incorrect_acc.login = "another_login"
            AccountManager(incorrect_acc)

        with pytest.raises(IncorrectPassword):
            incorrect_acc = copy(account)
            incorrect_acc.password = "another_password"
            AccountManager(incorrect_acc)



    def test_add_firm(self, firm:Firm, acc_crud:AccountCRUD, firm_crud:FirmCRUD):
        '''
        Тестирование метода по добавлению фирмы
        '''

        account = acc_crud.get_last_one()

        firm_m = FirmManager(firm=firm, 
                             account_id=account.id)
        assert firm_m.firm.id

        firms = firm_crud.get_all(account_id=account.id)
        assert firm_m.firm.id in firms

    

    def test_give_role(self, account:Account, firm_crud:FirmCRUD):
        '''
        Тестирование метода по выдаче роли аккаунту
        '''
        acc_m = AccountManager(account, send_code=False, new=True)

        firm = firm_crud.get_last_one()
        firm_m = FirmManager(firm)

        firm_m.give_role(account_id=acc_m.account.id,
                         role=Roles.admin.name)
        
        assert firm_crud.get_role(account_id=acc_m.account.id,
                                       firm_id=firm_m.firm.id) == Roles.admin.name
