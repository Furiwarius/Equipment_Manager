from app import app
from fastapi import status
import pytest
from fastapi.testclient import TestClient
from app.tests.fake_data import DataGenerator
from random import randrange
from copy import copy


class TestLoginAccountRoutes():
    '''
    Класс для тестирования ручек модуля login_account
    '''


    client = TestClient(app)
    generator = DataGenerator()



    @pytest.mark.asyncio
    async def test_index(self):
        '''
        Тестирование метода по получению индекскной страницы
        '''
        response = self.client.get("/")
        assert response.status_code == status.HTTP_200_OK



    @pytest.mark.asyncio
    async def test_registr(self):
        '''
        Тестирование метода по получению страницы регистрации
        '''
        response = self.client.get("/registr")
        assert response.status_code == status.HTTP_200_OK
    


    @pytest.mark.asyncio
    async def test_new_user(self):
        '''
        Тестирование метода по созданию нового пользователя
        '''
        new_acc = self.generator.account_generate()
        response = self.client.post("/registr",
                                    json={"login": new_acc.login,
                                          "email": new_acc.email,
                                          "password": new_acc.password,
                                          "timezone": str(new_acc.timezone)})
        
        assert response.status_code == status.HTTP_200_OK
        
        answer = response.json()
        assert answer["message"]=="Accaunt created"
    


    @pytest.mark.asyncio
    async def test_new_user_exception(self):
        '''
        Тестирование вызова исключений при использовании
        метода по созданию нового пользователя
        '''
        new_acc = self.generator.account_generate()
        json={"login": new_acc.login,
              "email": new_acc.email,
              "password": new_acc.password,
              "timezone": str(new_acc.timezone)}
        
        response = self.client.post("/registr", json=json)
        assert response.status_code == status.HTTP_200_OK
        
        for count, item in zip(range(2), json):

            copy_json = copy(json)
            copy_json[item]+=str(count)

            response = self.client.post("/registr", json=json)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



    @pytest.mark.asyncio
    async def test_autorization(self):
        '''
        Тестирование метода по получению страницы для авторизации
        '''
        response = self.client.get("/authorization")
        assert response.status_code == status.HTTP_200_OK
    


    @pytest.mark.asyncio
    async def test_login(self):
        '''
        Тестирование метода по авторизации пользователя
        '''
        acc = self.generator.account_generate()
        response_registr = self.client.post("/registr",
                                    json={"login": acc.login,
                                          "email": acc.email,
                                          "password": acc.password,
                                          "timezone": str(acc.timezone)})
        
        assert response_registr.status_code == status.HTTP_200_OK

        response = self.client.post("/login",
                                    json={"login": acc.login,
                                          "password": acc.password})
        
        assert response.status_code == status.HTTP_200_OK

        answer = response.json()
        assert answer["token"]
    


    @pytest.mark.asyncio
    async def test_login_exception(self):
        '''
        Тестирование метода по авторизации с получением исключений
        '''
        acc = self.generator.account_generate()
        response_registr = self.client.post("/registr",
                                    json={"login": acc.login,
                                          "email": acc.email,
                                          "password": acc.password,
                                          "timezone": str(acc.timezone)})
        
        assert response_registr.status_code == status.HTTP_200_OK

        json = {"login": acc.login, "password": acc.password}
        for item in json:
            copy_json = copy(json)
            copy_json[item]+=str(randrange(10))

            response = self.client.post("/login", json=copy_json)
            
            assert response.status_code == status.HTTP_401_UNAUTHORIZED