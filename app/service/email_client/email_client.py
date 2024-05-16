import smtplib
from configparser import ConfigParser
import jinja2

class EmailClient():
    '''
    Отправитель сообщений
    '''

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
        self.path_to_letter = config.get("setting letter", "path_to_letter")



    def __setting_letter(self, message:str) -> str:
        '''
        Настройка содержания пиьсма
        '''

        body = "\r\n".join((f"From: {self.user}", f"To: {self.to}", 
        f"Subject: {self.subject}", self.mime, self.charset, "", str(message)))

        return body
    

    def __send_bid(self, to, body_message:str) -> None:
        '''
        Отправка сообщения на почту
        '''
        smtp = smtplib.SMTP(self.server, self.port)
        smtp.starttls()
        smtp.ehlo()
        # логинимся на почтовом сервере
        smtp.login(self.user, self.passwd)
        # пробуем послать письмо
        smtp.sendmail(self.user, to, body_message.encode('utf-8'))
        smtp.quit()


    def render_letter(self, template:str, message:str) -> str:
        '''
        Вставка данных в шаблон
        '''

        filename = self.path_to_letter

        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        environment = jinja2.Environment()
        template = environment.from_string(template_file_content)
        letter = template.render(message=message)
        
        return letter


    def send (self, user_to:str, message:str) -> None:
        '''
        Главный метод-менеджер, генерирующий код, и отправляющий его на почту
        
        template - текстровый шаблон (путь до него), в который будет вставляться сообщение
        message - тест сообщения
        '''
        text_letter = self.render_letter(message)
        self.__send_bid(user_to, self.__setting_letter(text_letter))