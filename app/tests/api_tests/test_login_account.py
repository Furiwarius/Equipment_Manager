from fastapi import status
import pytest
from httpx import AsyncClient
from random import randrange
from copy import copy
from app.entities import Account


class TestLoginAccountRoutes():
    '''
    Класс для тестирования ручек модуля login_account
    '''



    @pytest.mark.asyncio
    async def test_index(self, async_client:AsyncClient):
        '''
        Тестирование метода по получению индекскной страницы
        '''
        response = await async_client.get("/")
        assert response.status_code == status.HTTP_200_OK



    @pytest.mark.asyncio
    async def test_registr(self, async_client:AsyncClient):
        '''
        Тестирование метода по получению страницы регистрации
        '''
        response = await async_client.get("/registr")
        assert response.status_code == status.HTTP_200_OK
    


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
    async def test_autorization(self, async_client:AsyncClient):
        '''
        Тестирование метода по получению страницы для авторизации
        '''
        response = await async_client.get("/authorization")
        assert response.status_code == status.HTTP_200_OK
    


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