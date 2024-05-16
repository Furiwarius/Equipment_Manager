import smtplib
from configparser import ConfigParser
import jinja2

class EmailClient():
    '''
    Отправитель сообщений
    '''

    default_template = "template_letter\default_template.txt"

    def __init__(self, 
                 setting=r"app\service\email_client\setting\setting.ini") -> None:
        # Если не был передан путь с настройками
        # то используется путь по умолчанию
        self.setting = setting
        self.__sender_settings()



    def __sender_settings(self) -> None:
        '''
        Чтение настроек из файла ini
        '''

        config = ConfigParser()
        config.read(self.setting)
            # Настройки
        self.mime = config.get("setting", "mime")
        self.charset = config.get("setting", "charset")
        self.server = config.get("setting", "server")
        self.port = config.get("setting", "port")

        self.user = config.get("personal data", "email")
        self.passwd = config.get("personal data", "passwd")

        self.subject = config.get("setting letter", "subject")



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
              template="template_letter\default_template.txt", ) -> None:
        '''
        Главный метод-менеджер, принимающий почту,
        на которую нужно отправить сообщение, само сообщение
        и шаблон для письма
        
        template - текстровый шаблон (путь до него), в который будет вставляться сообщение
        message - тест сообщения
        '''
        self.to = user_to
        self.filename = template
        text_letter = self.__render_letter(message)
        self.__send_bid(self.__setting_letter(text_letter))