from fastapi import status
import pytest
from httpx import AsyncClient
from random import randrange
from copy import copy
from app.entities import Account
from app.settings.settings import email_setting
from app.api.dependencies import verify_jwt_token


class TestLoginAccountRoutes():
    '''
    Класс для тестирования ручек модуля login_account
    '''



    @pytest.mark.asyncio
    async def test_new_user(self, account:Account, async_client:AsyncClient):
        '''
        Тестирование метода по созданию нового пользователя
        '''

        response = await async_client.post("/registr",
                                    json={"login": account.login,
                                          "email": account.email,
                                          "password": account.password,
                                          "timezone": str(account.timezone)})
        
        assert response.status_code == status.HTTP_200_OK    



    @pytest.mark.asyncio
    async def test_new_user_exception(self, account:Account, async_client:AsyncClient):
        '''
        Тестирование вызова исключений при использовании
        метода по созданию нового пользователя
        '''

        json={"login": account.login,
              "email": account.email,
              "password": account.password,
              "timezone": str(account.timezone)}
        
        response = await async_client.post("/registr", json=json)
        assert response.status_code == status.HTTP_200_OK
        
        for count, item in zip(range(2), json):

            copy_json = copy(json)
            copy_json[item]+=str(count)

            response = await async_client.post("/registr", json=json)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



    @pytest.mark.asyncio
    async def test_login(self, account:Account, async_client:AsyncClient):
        '''
        Тестирование метода по авторизации пользователя
        '''

        response_registr = await async_client.post("/registr",
                                    json={"login": account.login,
                                          "email": account.email,
                                          "password": account.password,
                                          "timezone": str(account.timezone)})
        
        assert response_registr.status_code == status.HTTP_200_OK

        response = await async_client.post("/login",
                                    json={"login": account.login,
                                          "password": account.password})
        
        assert response.status_code == status.HTTP_200_OK
    


    @pytest.mark.asyncio
    async def test_login_exception(self, account:Account, async_client:AsyncClient):
        '''
        Тестирование метода по авторизации с получением исключений
        '''

        response_registr = await async_client.post("/registr",
                                    json={"login": account.login,
                                          "email": account.email,
                                          "password": account.password,
                                          "timezone": str(account.timezone)})
        
        assert response_registr.status_code == status.HTTP_200_OK

        json = {"login": account.login, "password": account.password}
        for item in json:
            copy_json = copy(json)
            copy_json[item]+=str(randrange(10))

            response = await async_client.post("/login", json=copy_json)
            
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    


    # Тест проходт успешно, но поставлен флаг скип,
    # чтобы не спамить письмами на почту
    @pytest.mark.skip
    @pytest.mark.asyncio
    async def test_confirmation_code(self, async_client:AsyncClient):
        '''
        Тестрирование метода по получению кода
        '''
        response = await async_client.post("/confirmation_code", 
                                          json = {"email": email_setting.EMAIL})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["code"]
    


    # Тест проходт успешно, но поставлен флаг скип,
    # чтобы не спамить письмами на почту
    @pytest.mark.skip
    @pytest.mark.asyncio
    async def test_check_confirmation_code(self, async_client:AsyncClient):
        '''
        Тестирование отправки проверочного кода
        '''

        get_code_response = await async_client.post("/confirmation_code", 
                                          json = {"email": email_setting.EMAIL})

        assert get_code_response.status_code == status.HTTP_200_OK
        
        jwt = get_code_response.json()["code"]
        data = verify_jwt_token(jwt)

        response = await async_client.post("/check_confirmation_code", 
                                          json = {"code": data["code"],
                                                  "jwt": jwt})
        
        assert response.status_code == status.HTTP_200_OK

        