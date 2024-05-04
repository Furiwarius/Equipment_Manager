import smtplib
from configparser import ConfigParser
import random
import time


class SenderVerificationCode():
    '''
    Отправитель сообщений
    '''
    
    setting_path=r"app\service\user_account\verification_code\setting\email.ini"

    def __init__(self, __to_email:str) -> bool:

        self.sender_settings()
        self.__verification_code=None
        self.to = __to_email



    def sender_settings(self) -> None:
        '''
        Чтение настроек из файла ini
        '''

        config = ConfigParser()
        config.read(SenderVerificationCode.setting_path)
            # Настройки
        self.mime = config.get("setting", "mime")
        self.charset = config.get("setting", "charset")
        self.server = config.get("setting", "server")
        self.port = config.get("setting", "port")

        self.user = config.get("personal data", "email")
        self.passwd = config.get("personal data", "passwd")

        self.subject = config.get("setting letter", "subject")

        # рабочее время проверочного кода
        self.code_lifetime = config.get("verification code", "code_lifetime")



    def setting_letter(self, message:str) -> str:
        '''
        Настройка содержания пиьсма
        '''

        body = "\r\n".join((f"From: {self.user}", f"To: {self.to}", 
        f"Subject: {self.subject}", self.mime, self.charset, "", str(message)))

        return body
    

    def send_bid(self, body_message:str) -> None:
        '''
        Отправка сообщения на почту
        '''
        smtp = smtplib.SMTP(self.server, self.port)
        smtp.starttls()
        smtp.ehlo()
        # логинимся на почтовом сервере
        smtp.login(self.user, self.passwd)
        # пробуем послать письмо
        smtp.sendmail(self.user, self.to, body_message.encode('utf-8'))
        smtp.quit()


    def verification_code_generator(self) -> None:
        '''
        Метод генерирующий проверочный код
        '''
        # пятизначный код
        self.__verification_code = random.randrange(10000, 99999)
        # время генерации кода, выраженное в секундах с начала эпохи
        self.code_generation_time = time.time()
    

    def check_verification_code(self, code:int) -> bool:
        '''
        Метод сравнения проверочного кода
        '''
        if self.__verification_code==None or time.time()-self.code_generation_time>=self.code_lifetime:
            return False
        if self.__verification_code==code:
            return True
        return False



    def sending_verification_code (self) -> None:
        '''
        Главный метод-менеджер, генерирующий код, и отправляющий его на почту
        '''
        self.verification_code_generator()
        self.send_bid(self.setting_letter(self.__verification_code))