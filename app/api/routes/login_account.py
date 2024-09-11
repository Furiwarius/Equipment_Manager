from fastapi import APIRouter, Form, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from app.service.user_account.account import AccountManager, Account, AccountCRUD
from app.api.dependencies import create_jwt_token, verify_jwt_token, to_exist_account, to_new_account
from app.settings.settings import app_settings
from app.api.models.models import User, UserEmail, Code, AuthToken, TokenData, Token
from app.errors.service_error.account_error import (IncorrectInputData, LoginExists, CodeDoesntMatch, EmailExists)
from app.errors.base_exception import BaseApplicationException
from app.service.verification_code.code import SenderCode
from time import time
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated



login_account = APIRouter()


@login_account.get("/")
async def index():
    '''
    Главная страница
    '''
    return FileResponse("app/templates/index.html")



@login_account.post("/registr")
async def new_user(new_user: Annotated[Account, Depends(to_new_account)]):
    '''
    Регистрация пользователя
    '''
    try:
        AccountManager(account=new_user, new=True)
    
    except BaseApplicationException as err:
        raise HTTPException(status_code=422) from err
    
    return {"message": "Accaunt created"}



@login_account.post("/token")
async def login(user: Annotated[Account, Depends(to_exist_account)]) -> Token:
    '''
    Получение токена для пользователя
    '''
    try:
        acc: Account = AccountManager(account=user).account

    except IncorrectInputData as err:
        raise HTTPException(status_code=401, detail="Wrong login/password") from err
    
    token: str = create_jwt_token({"user_id": acc.id})

    return Token(access_token=token, token_type="bearer")



@login_account.post("/confirmation_code")
async def confirmation_code(email: UserEmail, sender:SenderCode = Depends(SenderCode)):
    '''
    При регистрации на сайте, будет отпревлен пятизначный код
    на почту, которую указал пользователь.
    '''
    confirmation_code = sender.send_code(email.email)

    code_token = create_jwt_token({"code": confirmation_code.code, "lifetime": confirmation_code.lifetime, "start_time": time()})
    
    return {"code": code_token}



@login_account.post("/check_confirmation_code")
async def check_confirmation_code(data:Code):
    '''
    Проверка кода подтверждения аккаунта
    '''
    
    try:
        jwt_data = verify_jwt_token(data.jwt)
    except HTTPException:
        raise HTTPException(status_code=419, detail="Incorrect token with source code")

    # Если истекло время ожидания кода
    if time()-int(jwt_data["start_time"])>int(jwt_data["lifetime"]):
        raise HTTPException(status_code=419, detail="Code lifetime has expired")
    
    # Если код неверный
    elif int(jwt_data["code"])!=int(data.code):
        raise HTTPException(status_code=419, detail="Wrong code")

    return {"message": "Email has been successfully verified"}



@login_account.get("/private_office")
async def private_office(token:AuthToken, 
                         acc_crud:AccountCRUD = Depends(AccountCRUD)):
    '''
    Личный кабинет
    '''
    try:
        acc_data:TokenData = verify_jwt_token(token.jwt)
    except HTTPException:
        raise HTTPException(status_code=419, detail="Invalid token")
    
    personal_data: Account = acc_crud.get_by_id(acc_data.user_id)
    
    return {"name":personal_data.login}