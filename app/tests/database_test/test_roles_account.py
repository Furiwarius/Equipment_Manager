from app.tests.fake_data import DataGenerator
from app.database.database import Database
from app.database.crud.firmCRUD import FirmCRUD
from app.database.crud.accountCRUD import AccountCRUD
from app.entities.account import Account


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

        self.account = self.acc_crud.add_account(new_account)

        assert self.account.id
    


    def test_confirm_account(self):
        '''
        Тестирование метода по подтверждению аккаунта
        '''
        
        account = self.acc_crud.get_last_one()

        assert not account.confirmation_status

        self.acc_crud.modify_status(account_id=account.id)