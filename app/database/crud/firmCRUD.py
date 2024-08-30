from app.database.tables.essence import FirmTable
from app.entities.firm import Firm
from app.database.crud.baseCRUD import BaseCRUD
from app.database.database import Database
from app.database.tables.summary import AccountRoles
from app.errors.database_error.database_error import ThisIsSuperAdmin
from app.errors.database_error.database_error import CannotGiveSuperadmin
from enum import Enum
from app.database.converter import convertertation



class Roles(Enum):
    '''
    Роли аккаунтов
    '''

    visitor="visitor"
    admin="admin"
    super_admin="super_admin"



class FirmCRUD(BaseCRUD):
    '''
    Класс для взаимодействия с бд 
    таблицей firm и связанных с ней

    Отвечает за создание фирм,
    назначение и выдачу ролей.
    '''



    def __init__(self) -> None:

        super().__init__(table=FirmTable)



    @convertertation
    @BaseCRUD.logger.info
    def add(self, account_id:int, new_firm:Firm) -> Firm:
        '''
        Добавить фирму

        Аккаунт, id которого передается, получает поль
        super_admin.
        '''

        with Database() as db:

            db.add(new_firm)     # добавляем в бд
            db.commit() 

            new_role = AccountRoles(firm_id = new_firm.id,
                                    account_id=account_id,
                                    role = Roles.super_admin.name)

            db.add(new_role)
            db.commit()     # сохраняем изменения

            result = db.query(self.table).order_by(self.table.id.desc()).first()
        return result



    # Этот метод находится тут, потому что нужно переопределить метод BaseCRUD.get_all
    # чтобы он искал по account_id, а не firm_id как у остальных круд-классов
    @convertertation
    @BaseCRUD.logger.info
    def get_all(self, account_id:int) -> dict:
        '''
        Получить список id фирм принадлежащих
        этому аккаунту с account_id

        Выдает только те id, где у аккаунта роль super_admin
        '''
        with Database() as db:
            firms_id = db.query(AccountRoles.firm_id).filter(AccountRoles.account_id==account_id,
                                                             AccountRoles.role==Roles.super_admin.name).all()

            return {item[0]:self.get_by_id(item[0]) for item in firms_id}

    

    @BaseCRUD.logger.info
    def give_role(self, account_id:int, firm_id:int, role:str) -> None:
        '''
        Выдать роль аккаунту
        
        Выдавать можно только роли админа или посетителя.
        В случае, если запись с ролью уже существует, и она
        не является ролью super_admin, то обновляется на новую.
        '''
        if role is Roles.super_admin.name:
            raise CannotGiveSuperadmin

        with Database() as db:
            
            check = db.query(AccountRoles).filter(AccountRoles.account_id==account_id,
                                                             AccountRoles.firm_id==firm_id).all()
            
            if not check:
                # Если такой записи не существует, то создает ее
                new_role = AccountRoles(firm_id = firm_id,
                                        account_id=account_id,
                                        role = role)   
                db.add(new_role)
            
            elif check and check[0].role==Roles.super_admin.name:
                raise ThisIsSuperAdmin

            else:
                db.query(AccountRoles).filter(AccountRoles.account_id==account_id,
                                              AccountRoles.firm_id==firm_id).update({
                                                  AccountRoles.role:role}, synchronize_session = False)

            db.commit()




    @BaseCRUD.logger.info
    def get_role(self, account_id:int, firm_id:int) -> str|None:
        '''
        Получить роль аккаунта для фирмы
        '''
        with Database() as db:
            check = db.query(AccountRoles).filter(AccountRoles.account_id==account_id,
                                                             AccountRoles.firm_id==firm_id).all()[0]

            if check:
                return check.role



