from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from app.service.firm.firm import Firm, FirmManager, FirmCRUD
from app.service.construction.construction import ConstructionCRUD
from app.api.dependencies import verify_jwt_token
from app.api.models.models import NewFirm


work_with_firm = APIRouter()
templates = Jinja2Templates(directory="app/templates")



@work_with_firm.get("/firms")
async def get_firms(token:str, firm_crud:FirmCRUD = Depends(FirmCRUD)):
    '''
    Страница со списком фирм, доступ к которым имеет аккаунт
    '''
    data = verify_jwt_token(token)
    if not data:
        raise HTTPException(status_code=419, detail="Invalid token")
    firms:list = firm_crud.get_all(data.get("user_id"))

    return {"firms": firms}



@work_with_firm.get("/firms/{firm_id}")
async def firm_info(firm_id:int, token:str, firm_crud:FirmCRUD = Depends(FirmCRUD)):
    '''
    Подробная страница фирмы
    '''
    data = verify_jwt_token(token)
    if not data:
        raise HTTPException(status_code=419, detail="Invalid token")
    
    if not firm_crud.get_role(data.get("user_id"), firm_id):
        # Если аккаунт не имеет любого доступа к фирме, то выдает исключение
        raise HTTPException(status_code=403, detail="This account does not have access to data")

    firm:Firm = firm_crud.get_by_id(firm_id)
        
    return {"firm": firm}



@work_with_firm.get("/firms/create_firm")
async def create_firm(request:Request, token:str):
    '''
    Страница для создания фирмы
    '''
    data = verify_jwt_token(token)
    if not data:
        raise HTTPException(status_code=419, detail="Invalid token")
        
    return templates.TemplateResponse("create_firm.html", {"request": request,
                                                    "page_name": "Создать фирму"})



@work_with_firm.post("/firms/create_firm")
async def create_firm(token:str, new_firm:NewFirm):
    '''
    Создание фирмы
    '''
    data = verify_jwt_token(token)
    if not data:
        raise HTTPException(status_code=419, detail="Invalid token")
    
    firm_manager = FirmManager(Firm(name=new_firm.name), data.get("user_id"))
    
    return {"firm": firm_manager.firm}



@work_with_firm.get("/firms/{firm_id}/constructions")
async def firm_constructions(firm_id:int, 
                             token:str, 
                             constr_crud:ConstructionCRUD = Depends(ConstructionCRUD),
                             firm_crud:FirmCRUD = Depends(FirmCRUD)):
    '''
    Список объектов фирмы
    '''
    data = verify_jwt_token(token)
    if not data:
        raise HTTPException(status_code=419, detail="Invalid token")
    
    elif not firm_crud.get_by_id(firm_id):
        raise HTTPException(status_code=404, detail="Not found")

    elif not firm_crud.get_role(data.get("user_id"), firm_id):
        # Если аккаунт не имеет любого доступа к фирме, то выдает исключение
        raise HTTPException(status_code=403, detail="This account does not have access to data")
    
    constructions:list = constr_crud.get_all(firm_id=firm_id)
        

    return {"constructions": constructions}