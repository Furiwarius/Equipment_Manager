from app.database.crud.firmCRUD import (FirmCRUD, Roles,
                                        ThisIsSuperAdmin, 
                                        CannotGiveSuperadmin)
import pytest
from app.database.crud.accountCRUD import AccountCRUD
from app.entities import Account, Firm



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
    


    def test_confirm_account(self, acc_crud:AccountCRUD):
        '''
        Тестирование метода по подтверждению аккаунта
        '''
        
        account = acc_crud.get_last_one()

        assert not account.confirmation_status

        acc_crud.modify_status(account_id=account.id)
        account = acc_crud.get_last_one()

        assert account.confirmation_status
    


    def test_get_account_by_login(self, account:Account, acc_crud:AccountCRUD):
        '''
        Тестирование метода получения аккаунта по логину
        '''

        account = acc_crud.add(account)
        assert account.id

        account_in_db = acc_crud.get_account_by_login(account.login)
        assert account_in_db.id==account.id



    def test_get_account_by_email(self, account:Account, acc_crud:AccountCRUD):
        '''
        Тестирование получения данных об аккаунте по адресу почты
        '''

        account = acc_crud.add(account)
        assert account.id

        account_in_db = acc_crud.get_account_by_email(account.email)
        assert account_in_db.id==account.id



    # Добавлять фирмы в бд можно только,
    # если есть аккаунт
    
    def test_add_firm(self, firm:Firm, acc_crud:AccountCRUD, firm_crud:FirmCRUD):
        '''
        Тестирование метода по добалению фирмы
        '''
        account = acc_crud.get_last_one()

        firm = firm_crud.add(account_id=account.id,
                                  new_firm=firm)
        
        assert firm.id



    def test_get_all_firm(self, account:Account, acc_crud:AccountCRUD, firm_crud:FirmCRUD):
        '''
        Тестирование метода по получению 
        списка id всех фирм аккаунта, где он super_admin
        '''

        account = acc_crud.get_last_one()
        firm = firm_crud.get_last_one()

        firms_id = firm_crud.get_all(account_id=account.id)

        assert firm.id in firms_id



    def test_give_role(self, account:Account, acc_crud:AccountCRUD, firm_crud:FirmCRUD):
        '''
        Тестирование метода по выдаче роли аккаунту
        '''

        last_account = acc_crud.get_last_one()
        firm = firm_crud.get_last_one()

        new_account = acc_crud.add(account)

        for role in (Roles.admin, Roles.visitor):
            firm_crud.give_role(account_id=new_account.id,
                                    firm_id=firm.id,
                                    role=role.name)
            
            assert role.name==firm_crud.get_role(account_id=new_account.id,
                                                            firm_id=firm.id)
        
        # Попытка назначить владельца фирмы на роль ниже суперадмина
        with pytest.raises(ThisIsSuperAdmin):
            firm_crud.give_role(account_id=last_account.id,
                                    firm_id=firm.id,
                                    role=Roles.admin.name)
        
        # Попытка назначить нового суперадмина
        with pytest.raises(CannotGiveSuperadmin):
            firm_crud.give_role(account_id=new_account.id,
                                    firm_id=firm.id,
                                    role=Roles.super_admin.name)