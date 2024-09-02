from app.database.crud.firmCRUD import (FirmCRUD, Roles,
                                        ThisIsSuperAdmin, 
                                        CannotGiveSuperadmin)
import pytest
from app.database.crud.accountCRUD import AccountCRUD
from app.entities import Account, Firm
from app.utilities.hashing import to_hash



class TestRoles():
    '''
    Класс для тестирования ролей и доступа
    '''


    def test_add_account(self, account:Account, acc_crud:AccountCRUD):
        '''
        Тестирование метода по добавлению аккаунта в БД
        '''

        account = acc_crud.add(account)

        assert account.id
    


    def test_confirm_account(self, exist_account:Account, acc_crud:AccountCRUD):
        '''
        Тестирование метода по подтверждению аккаунта
        '''
        
        assert not exist_account.confirmation_status

        acc_crud.modify_status(account_id=exist_account.id)

        account_in_db:Account = acc_crud.get_by_id(exist_account.id)

        assert account_in_db.confirmation_status
    


    def test_get_account_by_login(self, exist_account:Account, acc_crud:AccountCRUD):
        '''
        Тестирование метода получения аккаунта по логину
        '''

        account_in_db:Account = acc_crud.get_account_by_login(to_hash(exist_account.login))
        assert account_in_db.id==exist_account.id



    def test_get_account_by_email(self, exist_account:Account, acc_crud:AccountCRUD):
        '''
        Тестирование получения данных об аккаунте по адресу почты
        '''

        account_in_db:Account = acc_crud.get_account_by_email(exist_account.email)
        assert account_in_db.id==exist_account.id



    # Добавлять фирмы в бд можно только,
    # если есть аккаунт
    
    def test_add_firm(self, firm:Firm, exist_account:Account, firm_crud:FirmCRUD):
        '''
        Тестирование метода по добалению фирмы
        '''

        firm = firm_crud.add(account_id=exist_account.id,
                                  new_firm=firm)
        
        assert firm.id



    def test_get_all_firm(self, exist_account:Account, firm:Firm, firm_crud:FirmCRUD):
        '''
        Тестирование метода по получению 
        списка id всех фирм аккаунта, где он super_admin
        '''

        assert not firm_crud.get_all(account_id=exist_account.id)

        firm = firm_crud.add(account_id=exist_account.id,
                                  new_firm=firm)

        assert firm.id in firm_crud.get_all(account_id=exist_account.id)



    def test_give_role(self, exist_firm:Firm, exist_account:Account, firm_crud:FirmCRUD):
        '''
        Тестирование метода по выдаче роли аккаунту
        '''
        with pytest.raises(ThisIsSuperAdmin):
            for role in (Roles.admin, Roles.visitor):
                firm_crud.give_role(account_id=exist_account.id,
                                        firm_id=exist_firm.id,
                                        role=role.name)
                
                assert role.name==firm_crud.get_role(account_id=exist_account.id,
                                                                firm_id=exist_firm.id)