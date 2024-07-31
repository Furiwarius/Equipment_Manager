from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.service.firm.firm import Firm, FirmManager, FirmCRUD
from app.service.construction.construction import ConstructionCRUD
from app.api.dependencies import verify_jwt_token


work_with_firm = APIRouter()
templates = Jinja2Templates(directory="app/templates")
staticfiles = StaticFiles(directory="app")
work_with_firm.mount("/static", staticfiles, name="static")



@work_with_firm.get("/firms")
async def get_firms(request:Request, token:str, firm_crud:FirmCRUD = Depends(FirmCRUD)):
    '''
    Страница со списком фирм, доступ к которым имеет аккаунт
    '''
    data = verify_jwt_token(token)
    if not data:
        raise HTTPException(status_code=419, detail="Неправильный токен")
    firms:list = firm_crud.get_all(data.get("user_id"))

    return templates.TemplateResponse("firms.html", {"request": request,
                                                    "page_name": "Список фирм",
                                                    "firms": firms})



@work_with_firm.get("/firms/{firm_id}")
async def firm_info(request:Request, firm_id:int, token:str, firm_crud:FirmCRUD = Depends(FirmCRUD)):
    '''
    Подробная страница фирмы
    '''
    data = verify_jwt_token(token)
    if not data:
        raise HTTPException(status_code=419, detail="Неправильный токен")
    
    if not firm_crud.get_role(data.get("user_id"), firm_id):
        # Если аккаунт не имеет любого доступа к фирме, то выдает исключение
        raise HTTPException(status_code=403, detail="This account does not have access to data")

    firm:Firm = firm_crud.get_by_id(firm_id)
        
    return templates.TemplateResponse("firms.html", {"request": request,
                                                    "page_name": "Информация о фирме",
                                                    "firm": firm})



@work_with_firm.get("/firms/{firm_id}/constructions")
async def firm_constructions(request:Request, firm_id:int, token:str, constr_crud:ConstructionCRUD = Depends(ConstructionCRUD)):
    '''
    Список объектов фирмы
    '''
    data = verify_jwt_token(token)
    if not data:
        raise HTTPException(status_code=419, detail="Неправильный токен")
    
    constructions:list = constr_crud.get_all(firm_id=firm_id)
        

    return templates.TemplateResponse("firms.html", {"request": request,
                                                    "page_name": "Список строительных объектов",
                                                    "constructions": constructions})