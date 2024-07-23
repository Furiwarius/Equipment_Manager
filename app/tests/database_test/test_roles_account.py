from app.tests.fake_data import DataGenerator
from app.database.database import Database
from app.database.crud.firmCRUD import (FirmCRUD, Roles,
                                        ThisIsSuperAdmin, 
                                        CannotGiveSuperadmin)
from app.database.crud.accountCRUD import AccountCRUD
from app.entities.account import Account
import pytest


class TestRoles():
    '''
    Класс для тестирования ролей и доступа
    '''

    generator = DataGenerator()
    
    acc_crud = AccountCRUD()
    firm_crud = FirmCRUD()


    def test_add_account(self):
        '''
        Тестирование метода по добавлению аккаунта в БД
        '''

        new_account = self.generator.account_generate(status=False)

        self.account = self.acc_crud.add(new_account)

        assert self.account.id
    


    def test_confirm_account(self):
        '''
        Тестирование метода по подтверждению аккаунта
        '''
        
        account = self.acc_crud.get_last_one()

        assert not account.confirmation_status

        self.acc_crud.modify_status(account_id=account.id)
        account = self.acc_crud.get_last_one()

        assert account.confirmation_status
    


    def test_get_account_by_login(self):
        '''
        Тестирование метода получения аккаунта по логину
        '''

        account = self.acc_crud.add(self.generator.account_generate())
        assert account.id

        account_in_db = self.acc_crud.get_account_by_login(account.login)
        assert account_in_db.id==account.id



    def test_get_account_by_email(self):
        '''
        Тестирование получения данных об аккаунте по адресу почты
        '''

        account = self.acc_crud.add(self.generator.account_generate())
        assert account.id

        account_in_db = self.acc_crud.get_account_by_email(account.email)
        assert account_in_db.id==account.id


    # Добавлять фирмы в бд можно только,
    # если есть аккаунт
    
    def test_add_firm(self):
        '''
        Тестирование метода по добалению фирмы
        '''
        account = self.acc_crud.get_last_one()
        new_firm = self.generator.firm_generate()

        firm = self.firm_crud.add(account_id=account.id,
                                  new_firm=new_firm)
        
        assert firm.id



    def test_get_all_firm(self):
        '''
        Тестирование метода по получению 
        списка id всех фирм аккаунта, где он super_admin
        '''

        account = self.acc_crud.get_last_one()
        firm = self.firm_crud.get_last_one()

        firms_id = self.firm_crud.get_all(account_id=account.id)

        assert firm.id in firms_id

    

    def test_give_role(self):
        '''
        Тестирование метода по выдаче роли аккаунту
        '''

        account = self.acc_crud.get_last_one()
        firm = self.firm_crud.get_last_one()

        new_account = self.acc_crud.add(self.generator.account_generate())

        for role in (Roles.admin, Roles.visitor):
            self.firm_crud.give_role(account_id=new_account.id,
                                    firm_id=firm.id,
                                    role=role.name)
            
            assert role.name is self.firm_crud.get_role(account_id=new_account.id,
                                                            firm_id=firm.id)
        
        # Попытка назначить владельца фирмы на роль ниже суперадмина
        with pytest.raises(ThisIsSuperAdmin):
            self.firm_crud.give_role(account_id=account.id,
                                    firm_id=firm.id,
                                    role=Roles.admin.name)
        
        # Попытка назначить нового суперадмина
        with pytest.raises(CannotGiveSuperadmin):
            self.firm_crud.give_role(account_id=new_account.id,
                                    firm_id=firm.id,
                                    role=Roles.super_admin.name)