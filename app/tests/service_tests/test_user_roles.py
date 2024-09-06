from app.database.crud.accountCRUD import AccountCRUD, Account
from app.database.crud.firmCRUD import FirmCRUD, Roles
from app.service.user_account.account import AccountManager
from app.service.firm.firm import FirmManager, Firm
from app.errors.service_error.account_error import (IncorrectInputData, 
                                                    LoginExists, 
                                                    CodeDoesntMatch, 
                                                    EmailExists)
import pytest
from copy import copy
from random import randrange


class TestUserRoles():
    '''
    Тестирование работы классов FirmManager и AccountManager
    '''


    def test_add_new_account(self, account:Account):
        '''
        Тестирование метода по добавлению нового аккаунта
        '''
        account_m = AccountManager(account, new=True)


        assert account_m.account.id

    
    
    def test_add_exist_account(self, exist_account:Account):
        '''
        Тестирование метода по инициализации существующего аккаунта
        '''

        account_m:AccountManager = AccountManager(copy(exist_account))
        assert exist_account.id == account_m.account.id



    def test_exception_IncorrectPassword(self, exist_account:Account):
        '''
        Тестирование вызова исключения IncorrectInputData
        неправильным паролем при работе с AccuntManager
        '''
        with pytest.raises(IncorrectInputData):
            exist_account.password+="string"
            AccountManager(exist_account)



    def test_exception_IncorrectLogin(self, exist_account:Account):
        '''
        Тестирование вызова исключения IncorrectInputData
        неправильным логином при работе с AccuntManager
        '''
        with pytest.raises(IncorrectInputData):
            exist_account.login+="string"
            AccountManager(exist_account)



    def test_exception_EmailExists(self, exist_account:Account):
        '''
        Тестирование вызова исключения EmailExists 
        при работе с AccuntManager
        '''
        with pytest.raises(EmailExists):
            exist_account.login+="string"
            AccountManager(exist_account, new=True)



    def test_exception_LoginExists(self, exist_account:Account):
        '''
        Тестирование вызова исключения LoginExists 
        при работе с AccuntManager
        '''
        with pytest.raises(LoginExists):
            exist_account.email+="string"
            AccountManager(exist_account, new=True)



    def test_add_firm(self, firm:Firm, exist_account:Account, firm_crud:FirmCRUD):
        '''
        Тестирование метода по добавлению фирмы
        '''

        firm_m = FirmManager(firm=firm, 
                             account_id=exist_account.id)
        assert firm_m.firm.id

        firms = firm_crud.get_all(account_id=exist_account.id)
        assert firm_m.firm.id in firms
