from typing_extensions import Annotated, Doc
from fastapi.param_functions import Form
import jwt
from datetime import datetime, timezone
from app.settings.settings import jwt_settings
from fastapi import HTTPException, Depends, status
from app.api.models.models import TokenData
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from app.errors.api_error.token_error import InvalidToken
from app.entities.account import Account



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):

    def __init__(self, *, grant_type: str | None = None, username: str, password: str, email:str, timezone:str, scope: str = "", client_id: str | None = None, client_secret: str | None = None):
        self.email: str = email
        self.timezone: str = timezone
        
        super().__init__(grant_type=grant_type, username=username, password=password, scope=scope, client_id=client_id, client_secret=client_secret)



def create_jwt_token(data: dict) -> str:
    '''
    Создание токена из словаря данных
    '''
    # Время жизни токена
    expiration = datetime.now(timezone.utc) + jwt_settings.EXPIRATION_TIME
    # Добавляем в тело токена время жизни
    data.update({"exp": expiration})

    token = jwt.encode(data, jwt_settings.JWT_KEY, algorithm=jwt_settings.ALGORITHM)
    
    return token



def verify_jwt_token(token: str) -> TokenData:
    '''
    Расшифровка токена
    '''
    try:
        decoded_data = jwt.decode(token, 
                                  jwt_settings.JWT_KEY, 
                                  algorithms=[jwt_settings.ALGORITHM])
        
        return TokenData(user_id=decoded_data["user_id"])
    
    except jwt.PyJWTError:
        raise InvalidToken
    



async def getting_data(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    '''
    Получение данных из токена
    '''
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        data:TokenData = verify_jwt_token(token)
    except InvalidToken:
        raise credentials_exception
    
    return data



async def get_current_user(current_user: Annotated[TokenData, Depends(getting_data)]) -> TokenData:
    '''
    Получение пользователя по токену
    '''
    
    return current_user



async def to_exist_account(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Account:
    '''
    Формирование экземпляра entities из данных форм
    '''
    
    return Account(login=form_data.username, password=form_data.password)



async def to_new_account(form_data: CustomOAuth2PasswordRequestForm = Depends()) -> Account:
    '''
    Формирование экземпляра entities из данных форм
    '''

    return Account(login=form_data.username,
                   password=form_data.password, 
                   email=form_data.email, 
                   timezone=form_data.timezone)