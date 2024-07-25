from app.database.crud.firmCRUD import FirmCRUD, Roles
from app.entities.firm import Firm
from app.service.validator.validator import ValidatorEssence, DataValidator
from app.errors.service_error.firm_error import IdNotSent, WrongRolePassed


class FirmManager():
    '''
    Управляющий класс для фирмы
    '''

    # Классы валидаторы
    valid_essence = ValidatorEssence()
    valid_data = DataValidator()


    def __init__(self, firm:Firm, account_id:int = None) -> None:
        '''
        При передаче constr взятого из БД
        продолжает с ним рабоать.
        Если объект новый, то пытается добавить его в БД.
        '''

        self.firm_crud = FirmCRUD()


        if firm.id is None:
            if account_id is None:
                # При создании новой фирмы нужно передавать также account_id
                raise IdNotSent
            
            self.valid_essence.validate_firm(firm)
            
            self.firm=self.firm_crud.add(account_id=account_id,
                                         new_firm=firm)

        else:
            self.firm = firm  
    

    
    def give_role(self, account_id:int, role:Roles) -> None:
        '''
        Выдать роль аккаунту
        '''
       
        if role!=Roles.admin.name or role!=Roles.visitor.name:
            raise WrongRolePassed
        

        self.firm_crud.give_role(account_id=account_id,
                                 firm_id=self.firm.id,
                                 role=role)



    
