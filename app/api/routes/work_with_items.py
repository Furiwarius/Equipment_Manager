from fastapi import APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from app.service.firm.firm import FirmCRUD
from app.service.construction.construction import ConstructionCRUD, Construction, ConstructionManager
from app.api.dependencies import verify_jwt_token
from app.api.models.models import NewConstruction
from datetime import datetime, timezone


work_with_items = APIRouter()
templates = Jinja2Templates(directory="app/templates")



@work_with_items.get("/firms/{firm_id}/constructions/{constr_id}")
async def constr_info(constr_id: int,
                    firm_id: int,
                    token: str, 
                    firm_crud: FirmCRUD = Depends(FirmCRUD),
                    constr_crud: ConstructionCRUD = Depends(ConstructionCRUD)):
    '''
    Подробная страница объекта строительства
    '''
    data = verify_jwt_token(token)
    
    if not firm_crud.get_role(data.get("user_id"), firm_id):
        # Если аккаунт не имеет любого доступа к фирме, то выдает исключение
        raise HTTPException(status_code=403, detail="This account does not have access to data")

    constr: Construction = constr_crud.get_by_id(constr_id)

    if constr is None:
        raise HTTPException(status_code=404, detail="Not found")
    
    elif constr.firm_id!=firm_id:
        raise HTTPException(status_code=403, detail="Object belongs to another company")

    return {"construction": constr}



@work_with_items.get("/firms/{firm_id}/constructions/create")
async def create_constr(new_constr: NewConstruction,
                    firm_id: int,
                    token: str, ):
    '''
    Подробная страница объекта строительства
    '''
    data = verify_jwt_token(token)
    
    access_to_changes(firm_id, data.get("user_id"))

    constr = Construction(firm_id=firm_id,
                          name=new_constr.name,
                          address=new_constr.address,
                          project=new_constr.project,
                          start_date=datetime.now(timezone.utc))
    constr_m = ConstructionManager(constr)
    
    return {"construction": constr_m.constr}



def access_to_changes(firm_id:int, user_id:int, firm_crud: FirmCRUD = Depends(FirmCRUD)):
    '''
    Проверка прав доступа на добавление
    или модификацию элементов фирмы
    '''
    role: str = firm_crud.get_role(user_id, firm_id)
    if role != "admin" and role != "super_admin":
        # Если у аккаунта роль ниже админа или суперадмина, то выдает исключение
        raise HTTPException(status_code=403, detail="This account does not have access to data")