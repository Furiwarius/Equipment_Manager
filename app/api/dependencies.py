import jwt
from datetime import datetime, timezone
from app.settings.settings import jwt_settings
from fastapi import HTTPException


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



def verify_jwt_token(token: str) -> dict:
    '''
    Расшифровка токена
    '''
    try:
        decoded_data = jwt.decode(token, 
                                  jwt_settings.JWT_KEY, 
                                  algorithms=[jwt_settings.ALGORITHM])
        return decoded_data
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=419, detail="Invalid token")