import smtplib
import jinja2
from app.settings.settings import email_setting



class EmailClient():
    '''
    Отправитель сообщений
    '''


    def __init__(self) -> None:
        # Если не был передан путь с настройками
        # то используется путь по умолчанию
        self.__sender_settings()
        self.user = email_setting.EMAIL
        self.passwd = email_setting.PASSWORD



    def __sender_settings(self) -> None:
        '''
        Чтение настроек из файла ini
        '''

        # Настройки
        self.mime = email_setting.mime
        self.charset = email_setting.charset
        self.server = email_setting.server
        self.port = email_setting.port



    def __setting_letter(self, message:str) -> str:
        '''
        Настройка содержания пиьсма
        '''

        body = "\r\n".join((f"From: {self.user}", f"To: {self.to}", 
        f"Subject: {self.subject}", self.mime, self.charset, "", str(message)))

        return body
    


    def __send_bid(self, body_message:str) -> None:
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



    def __render_letter(self, message:str) -> str:
        '''
        Вставка данных в шаблон
        '''

        with open(self.filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        environment = jinja2.Environment()
        template = environment.from_string(template_file_content)
        letter = template.render(message=message)
        
        return letter



    def send (self, user_to:str, message:str,
              template=email_setting.default_template, subject="new letter") -> None:
        '''
        Главный метод-менеджер, принимающий почту,
        на которую нужно отправить сообщение, само сообщение
        и шаблон для письма
        
        template - текстовый шаблон (путь до него), в который будет вставляться сообщение
        message - тест сообщения
        '''
        self.to = user_to
        self.filename = template
        self.subject = subject

        text_letter = self.__render_letter(message)
        self.__send_bid(self.__setting_letter(text_letter))