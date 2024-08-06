from fastapi import Depends, HTTPException
from app.database.crud.firmCRUD import FirmCRUD



def access_to_changes(firm_id:int, user_id:int, firm_crud: FirmCRUD = Depends(FirmCRUD)):
    '''
    Проверка прав доступа на добавление
    или модификацию элементов фирмы
    '''
    role: str = firm_crud.get_role(user_id, firm_id)
    if role != "admin" and role != "super_admin":
        # Если у аккаунта роль ниже админа или суперадмина, то выдает исключение
        raise HTTPException(status_code=403, detail="This account does not have access to data")
    


def access_to_visit(firm_id:int, user_id:int, firm_crud: FirmCRUD = Depends(FirmCRUD)):
    '''
    Проверка прав доступа на просмотр элементов фирмы
    '''
    role: str = firm_crud.get_role(user_id, firm_id)
    if not role:
        # Если у аккаунта отсутствует роль для данной фирмы, то выдает исключение
        raise HTTPException(status_code=403, detail="This account does not have access to data")