from configparser import ConfigParser
from app.clients.email_client.email_client import EmailClient
import random
import time
from os import path


class SenderCode():
    '''
    Отправитель сообщений
    '''

    setting_code = r"app\setting\setting_code.ini"


    def __init__(self, __to_email:str) -> bool:

        self.__sender_settings()
        self.__code=self.__code_generator()
        self.__to = __to_email
        self.__email = EmailClient(path.abspath(self.__setting_email))


    def __sender_settings(self) -> None:
        '''
        Чтение настроек из файла ini
        '''

        config = ConfigParser()
        config.read(SenderCode.setting_code)

            # Настройки
        self.__code_lifetime = config.get("verification code", "code_lifetime")

        # в настройках хранятся относительные пути к файлам
        # с помощью path.abspath(...) отправляется абсолютный путь
        self.__setting_email = config.get("setting sender", "setting_emailclient")
        self.__template = config.get("setting sender", "setting_emailclient")


    def __code_generator(self) -> None:
        '''
        Метод генерирующий проверочный код
        '''
        # пятизначный код
        self.__code = random.randrange(10000, 99999)
        # время генерации кода, выраженное в секундах с начала эпохи
        self.code_generation_time = time.time()
    

    def check_code(self, code:int) -> bool:
        '''
        Метод сравнения проверочного кода
        '''
        if time.time()-self.code_generation_time>=self.__code_lifetime:
            return False
        if self.__code==code:
            return True
        return False


    def send_code (self) -> None:
        '''
        Главный метод-менеджер, генерирующий код, и отправляющий его на почту
        '''
        self.__email.send(user_to=self.__to, 
                          message=self.__code,
                          template=path.abspath(self.__template))