from app.clients.email_client.email_client import EmailClient
import random
import time
from os import path
from collections import namedtuple
from app.settings.settings import code_setting



class SenderCode():
    '''
    Отправитель сообщений
    '''


    # Класс, который отправляет метод send_code()
    Code = namedtuple("Code", ["code", "lifetime"])


    def __init__(self, __to_email:str) -> bool:

        self.__sender_settings()
        self.code = random.randrange(10000, 99999)
        self.__to = __to_email
        self.__email = EmailClient()



    def __sender_settings(self) -> None:
        '''
        Чтение настроек из файла ini
        '''

        # Настройки
        self.code_lifetime = code_setting.lifetime

        # в настройках хранятся относительные пути к файлам
        # с помощью path.abspath(...) отправляется абсолютный путь
        self.__template = code_setting.template_letter



    def send_code (self) -> Code:
        '''
        Главный метод-менеджер, генерирующий код, и отправляющий его на почту
        '''
        self.__email.send(user_to = self.__to, 
                          message = self.code,
                          template = path.abspath(self.__template),
                          subject = code_setting.subject_letter)
        
        return SenderCode.Code(code=self.code, lifetime=self.code_lifetime)